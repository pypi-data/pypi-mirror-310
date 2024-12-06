from __future__ import annotations

import copy
import logging
import multiprocessing
import os
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any

import awkward as ak
import torch
import uproot
from torch.utils.data import DataLoader, IterableDataset

from f9columnar.processors import Processor, ProcessorsGraph
from f9columnar.utils.helpers import get_file_size


@dataclass
class RootFile:
    file_name: str
    key: str

    file_size: float = 0.0
    num_entries: int = 0
    tree: uproot.TTree = None

    def __post_init__(self) -> None:
        if not os.path.exists(self.file_name):
            raise RuntimeError(f"File {self.file_name} does not exist.")

        if not os.path.isfile(self.file_name):
            raise RuntimeError(f"{self.file_name} is not a file.")

        if not self.file_name.endswith(".root"):
            raise ValueError(f"File {self.file_name} is not a ROOT file.")

        self.file_size = get_file_size(self.file_name)

        self.file_name = f"{self.file_name}:{self.key}"

    def open(self) -> uproot.TTree:
        self.tree = uproot.open(self.file_name)
        self.num_entries = self.tree.num_entries
        return self


@dataclass
class RootFiles:
    file_names: list[str]
    key: str | list[str]

    files_dct: dict[str, RootFile] = field(default_factory=dict)

    file_size_dct: dict[str, float] = field(default_factory=dict)
    num_entries_dct: dict[str, int] = field(default_factory=dict)

    total_file_size: float = 0.0
    total_num_entries: int = 0

    def __post_init__(self) -> None:
        for i, file_name in enumerate(self.file_names):
            if type(self.key) is list:
                root_file = RootFile(file_name, self.key[i])
            elif type(self.key) is str:
                root_file = RootFile(file_name, self.key)
            else:
                raise ValueError(f"Key {self.key} is not a valid type.")

            root_file = root_file.open()

            self.files_dct[file_name] = root_file

            self.file_size_dct[file_name] = root_file.file_size
            self.num_entries_dct[file_name] = root_file.num_entries

            self.total_file_size += root_file.file_size
            self.total_num_entries += root_file.num_entries

    def __getitem__(self, file_name: str) -> RootFile:
        return self.files_dct[file_name]


class UprootIterator:
    def __init__(
        self,
        root_file: RootFile,
        step_size: int,
        filter_name: Callable[[str], bool] | None = None,
        entry_start: int | None = None,
        entry_stop: int | None = None,
        **kwargs: Any,
    ) -> None:
        if type(step_size) is not int:
            raise ValueError(f"Step size {step_size} is not an integer.")

        self.root_file = root_file
        self.step_size = step_size
        self.filter_name = filter_name
        self.kwargs = kwargs

        num_entries = self.root_file.num_entries

        # assign start and stop entries
        if entry_start is None:
            self.entry_start = 0
        else:
            self.entry_start = entry_start

        if entry_stop is None:
            self.entry_stop = num_entries
        else:
            self.entry_stop = entry_stop

        # handle cases where step size is larger than the number of entries
        if self.entry_start is not None and self.entry_stop is not None:
            delta_entry = self.entry_stop - self.entry_start

            if self.step_size > delta_entry:
                self.step_size = delta_entry
        else:
            if self.step_size > num_entries:
                self.step_size = num_entries

        self.tree: uproot.TTree = None
        self.returned_iterator = False

    def get_iterator(self) -> Iterator[tuple[ak.Array, Any]]:
        if self.root_file.tree is None:
            self.tree = uproot.open(self.root_file.file_name)
        else:
            self.tree = self.root_file.tree

        uproot_iterator = self.tree.iterate(
            library="ak",
            report=True,
            step_size=self.step_size,
            filter_name=self.filter_name,
            entry_start=self.entry_start,
            entry_stop=self.entry_stop,
            **self.kwargs,
        )

        self.returned_iterator = True

        return uproot_iterator

    def close(self) -> None:
        self.tree.close()


class UprootIteratorMaker:
    def __init__(
        self,
        name: str,
        files: list[str],
        key: str | list[str],
        step_size: int,
        num_workers: int,
        filter_name: Callable[[str], bool] | None = None,
        **kwargs: Any,
    ) -> None:
        self.name = name
        self.files, self.key = files, key
        self.num_workers = num_workers
        self.step_size = step_size
        self.filter_name = filter_name
        self.kwargs = kwargs

        self.total_num_entries = 0

    def _log_info(self, total_files_size: float, total_num_entries: int) -> None:
        info_str = "\n" + 15 * "=" + " info " + 15 * "="
        info_str += f"\nName: {self.name}\n"
        info_str += f"Number of ROOT files: {len(self.files)}\n"
        info_str += f"Total size: {total_files_size:.3f} GB\n"
        info_str += f"Total number of entries: {total_num_entries}\n"
        info_str += 36 * "="

        logging.info(info_str)

    def _make_iterator(self, root_file: RootFile, entry_start: int, entry_stop: int) -> UprootIterator:
        return UprootIterator(
            root_file,
            step_size=self.step_size,
            filter_name=self.filter_name,
            entry_start=entry_start,
            entry_stop=entry_stop,
            **self.kwargs,
        )

    def make(self) -> list[list[UprootIterator]]:
        root_files = RootFiles(self.files, self.key)

        self._log_info(root_files.total_file_size, root_files.total_num_entries)

        total_num_entries = root_files.total_num_entries
        self.total_num_entries = total_num_entries

        # how many entries each worker will process
        splits = [total_num_entries // self.num_workers] * self.num_workers
        splits[-1] += total_num_entries % self.num_workers

        all_num_entries_dct = root_files.num_entries_dct
        num_entries_dct = copy.deepcopy(root_files.num_entries_dct)

        # keep track of the start and stop entries for each root file
        root_files_start_dct: dict[str, int] = {root_file: 0 for root_file in self.files}

        result: list[dict[str, list[int]]] = [{} for _ in range(len(splits))]

        done = []
        for i, split in enumerate(splits):

            total = 0
            for root_file, num_entries in num_entries_dct.items():
                if root_file in done:
                    continue

                start_entry = root_files_start_dct[root_file]

                total += num_entries

                if total <= split:
                    result[i][root_file] = [start_entry, all_num_entries_dct[root_file]]
                    done.append(root_file)

                    if total == split:
                        break
                    else:
                        continue

                if total > split:
                    delta = num_entries - (total - split)
                    result[i][root_file] = [start_entry, start_entry + delta]
                    root_files_start_dct[root_file] += delta
                    num_entries_dct[root_file] -= delta
                    break

        worker_uproot_iterators: list[list] = [[] for _ in range(self.num_workers)]
        check_total = 0

        for i, result_dct in enumerate(result):
            for root_file, start_end in result_dct.items():
                entry_start, entry_end = start_end
                check_total += entry_end - entry_start

                iterator = self._make_iterator(root_files[root_file], entry_start, entry_end)
                worker_uproot_iterators[i].append(iterator)

        if check_total != total_num_entries:
            raise ValueError("Total number of entries does not match.")

        return worker_uproot_iterators


class RootLoaderIterator:
    def __init__(
        self,
        name: str,
        uproot_iterators: list[UprootIterator],
        worker_id: int,
        processors: list[Callable[[ak.Array, dict], tuple[ak.Array, dict]]] | ProcessorsGraph | None = None,
        root_files_desc_dct: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.name = name
        self.uproot_iterators = uproot_iterators
        self.worker_id = worker_id
        self.processors = processors
        self.root_files_desc_dct = root_files_desc_dct

        self.current_iterator: Iterator[tuple[ak.Array, Any]]
        self.current_iterator_idx = 0

    def _run_processors(self, arrays: ak.Array, reports: dict) -> tuple[ak.Array, dict] | dict[str, Processor]:
        if self.processors is None:
            return arrays, reports
        elif type(self.processors) is list:
            for proc in self.processors:
                arrays, reports = proc(arrays, reports)
            return arrays, reports
        elif type(self.processors) is ProcessorsGraph:
            processors = self.processors.fit(arrays, reports)
            return processors
        else:
            raise ValueError(f"Processors {self.processors} is not a valid type.")

    def _make_report(self, reports: Any) -> dict:
        file_path = reports._source._file._file_path
        file_name = os.path.basename(file_path)
        start, stop = reports._tree_entry_start, reports._tree_entry_stop

        reports = {
            "name": self.name,
            "worker_id": self.worker_id,
            "file_path": file_path,
            "file": file_name,
            "start": start,
            "stop": stop,
        }

        if self.root_files_desc_dct is not None:
            reports = reports | self.root_files_desc_dct[file_name]

        return reports

    def __iter__(self) -> RootLoaderIterator:
        return self

    def __next__(self) -> tuple[ak.Array, dict] | dict[str, Processor]:
        try:
            uproot_iterator = self.uproot_iterators[self.current_iterator_idx]

            if uproot_iterator.returned_iterator is False:
                self.current_iterator = uproot_iterator.get_iterator()

            arrays, reports = next(self.current_iterator)

        except StopIteration:
            uproot_iterator.close()
            self.current_iterator_idx += 1

            if self.current_iterator_idx == len(self.uproot_iterators):
                raise StopIteration
            else:
                uproot_iterator = self.uproot_iterators[self.current_iterator_idx]
                self.current_iterator = uproot_iterator.get_iterator()
                arrays, reports = next(self.current_iterator)

        reports = self._make_report(reports)

        processors_return = self._run_processors(arrays, reports)

        return processors_return


class RootIterableDataset(IterableDataset):
    def __init__(
        self,
        name: str,
        worker_uproot_iterators: list[list[UprootIterator]],
        processors: list[Callable[[ak.Array, dict], tuple[ak.Array, dict]]] | ProcessorsGraph | None = None,
        root_files_desc_dct: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.name = name
        self.worker_uproot_iterators = worker_uproot_iterators
        self.processors = processors
        self.root_files_desc_dct = root_files_desc_dct

    def __iter__(self) -> RootLoaderIterator:
        worker_info = torch.utils.data.get_worker_info()

        if worker_info is None:
            worker_id = 0
        else:
            worker_id = worker_info.id

        uproot_iterators = self.worker_uproot_iterators[worker_id]

        return RootLoaderIterator(
            self.name,
            uproot_iterators,
            worker_id,
            processors=self.processors,
            root_files_desc_dct=self.root_files_desc_dct,
        )


def get_root_dataloader(
    name: str,
    files: list[str],
    key: str,
    step_size: int,
    num_workers: int,
    processors: list[Callable[[ak.Array, dict], tuple[ak.Array, dict]]] | ProcessorsGraph | None = None,
    filter_name: Callable[[str], bool] | None = None,
    root_files_desc_dct: dict[str, dict[str, Any]] | None = None,
    uproot_kwargs: dict[str, Any] | None = None,
    dataloader_kwargs: dict[str, Any] | None = None,
) -> tuple[DataLoader, int]:

    if num_workers == -1:
        num_workers = multiprocessing.cpu_count()

    if uproot_kwargs is None:
        uproot_kwargs = {}

    if dataloader_kwargs is None:
        dataloader_kwargs = {}

    logging.info("Making ROOT dataloader!")

    uproot_iterator_maker = UprootIteratorMaker(
        name,
        files,
        key,
        step_size,
        num_workers,
        filter_name=filter_name,
        **uproot_kwargs,
    )
    worker_uproot_iterators = uproot_iterator_maker.make()

    total_num_entries = uproot_iterator_maker.total_num_entries

    root_iterable_dataset = RootIterableDataset(
        name,
        worker_uproot_iterators,
        processors=processors,
        root_files_desc_dct=root_files_desc_dct,
    )

    root_dataloader = DataLoader(
        root_iterable_dataset,
        batch_size=None,
        num_workers=num_workers,
        prefetch_factor=None,
        **dataloader_kwargs,
    )

    return root_dataloader, total_num_entries
