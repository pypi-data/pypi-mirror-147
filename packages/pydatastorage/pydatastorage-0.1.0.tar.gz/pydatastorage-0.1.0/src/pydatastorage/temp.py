import os
from hashlib import md5, sha256
from pathlib import Path
from typing import Iterator, Optional, Type, Union
from types import TracebackType
from tempfile import TemporaryDirectory
from pathlib import Path

from contextlib import AbstractContextManager

from pydantic import Field, PrivateAttr

from . import DataStorage, DataID, DirectoryDataStorage


class TempDataStorage(DataStorage, AbstractContextManager):
    muuid = "2ffb39fb-2fea-4dae-b3e3-1bb610904b29"
    _tmp_dir: TemporaryDirectory = PrivateAttr()
    _ds: DirectoryDataStorage = PrivateAttr()
    prefix: Optional[str]

    def __init__(self, prefix: Optional[str] = None):
        super().__init__(prefix=prefix)
        self._tmp_dir = TemporaryDirectory(prefix=prefix)
        self._ds = DirectoryDataStorage(path=self._tmp_dir.name)

    def is_valid(self) -> bool:
        return Path(self._tmp_dir.name).is_dir() and self._ds.is_valid()

    def has(self, h: Optional[DataID]) -> bool:
        return self._ds.has(h)

    def get(self, h: DataID) -> bytes:
        return self._ds.get(h)

    def store(self, data: bytes) -> DataID:
        return self._ds.store(data)

    def remove(self, h: DataID) -> bool:
        return self._ds.remove(h)

    def purge(self) -> bool:
        if self.is_valid():
            self._tmp_dir.cleanup()
            return True
        return False

    def __iter__(self) -> Iterator[DataID]:
        return iter(self._ds)

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        self.purge()
        return None

