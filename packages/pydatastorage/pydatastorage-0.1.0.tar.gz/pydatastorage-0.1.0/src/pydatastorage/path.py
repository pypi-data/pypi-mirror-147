import hashlib
import os
from pathlib import Path
from typing import Iterator, Optional, Union

from . import DataStorage, DataID


def hash_path(h: DataID) -> Path:
    return Path(".") / h[:2] / h[2:4] / h[4:8] / h[8:]


class DirectoryDataStorage(DataStorage):
    muuid = "11ffc9f4-1a7a-4e13-8a28-ab78d8364f27"
    path: Path

    def __init__(self, path: Path):
        super().__init__(path=path)

    def is_valid(self) -> bool:
        if self.path.exists() and not self.path.is_dir():
            return False
        if not self.path.exists():
            try:
                self.path.mkdir(parents=True, exist_ok=True)
            except IOError:
                return False
        return True

    def has(self, h: Optional[DataID]) -> bool:
        if h is None:
            return False
        file = self.path / hash_path(h)
        return file.exists()

    def get(self, h: DataID) -> bytes:
        file = self.path / hash_path(h)
        return file.read_bytes()

    def store(self, data: bytes) -> DataID:
        h = DataID(hashlib.sha256(data).hexdigest())
        file = self.path / hash_path(h)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(data)
        return h

    def remove(self, h: DataID) -> bool:
        file = self.path / hash_path(h)
        if file.exists():
            os.remove(file)
        while file.parent != self.path:
            file = file.parent
            if file.exists():
                if len(list(file.iterdir())) > 0:
                    break
                file.rmdir()
        return True

    def __iter__(self) -> Iterator[DataID]:
        return iter(set(DataID(f.name) for f in self.path.glob("**") if self.has(DataID(f.name))))

