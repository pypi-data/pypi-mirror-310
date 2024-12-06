from collections.abc import Hashable, Iterable
from pathlib import Path

from .tsvreader import TSVReader


class DataLoader:
    @staticmethod
    def load_data(
        data_dir: Path,
        keys: Iterable[Hashable],
        data_files: Iterable[str],
    ) -> dict[Hashable, TSVReader]:
        data = {}
        for key, data_file in zip(keys, data_files, strict=True):
            data[key] = TSVReader(data_dir / data_file)

        return data
