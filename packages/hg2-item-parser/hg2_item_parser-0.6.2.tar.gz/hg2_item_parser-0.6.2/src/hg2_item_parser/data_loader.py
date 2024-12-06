from collections.abc import Hashable, Iterable
from pathlib import Path

from .tsvreader import TSVReader


class DataLoader:
    @staticmethod
    def load_data(
        data_dir_path: Path,
        keys: Iterable[Hashable],
        data_file_names: Iterable[str],
    ) -> dict[Hashable, TSVReader]:
        data = {}
        for key, data_file_name in zip(keys, data_file_names, strict=True):
            data[key] = TSVReader(data_dir_path / data_file_name)

        return data
