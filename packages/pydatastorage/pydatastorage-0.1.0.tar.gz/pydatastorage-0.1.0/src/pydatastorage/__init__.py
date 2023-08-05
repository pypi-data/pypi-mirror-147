__version__ = "0.1.0"

from typing import Iterator, Optional
from pydantic_uuid_model import UUIDBaseModel  # type: ignore[import]


__all__ = [
    "DataID",
    "DataStorage",
    "DirectoryDataStorage",
    "RemoteDataStorage",
    "TempDataStorage",
]


class DataID(str):
    pass


class DataStorage(UUIDBaseModel, base=True):  # type: ignore[call-arg]

    def is_valid(self) -> bool:
        return False

    def has(self, h: Optional[DataID]) -> bool:
        return h is not None and self.get(h) is not None

    def get(self, h: DataID) -> bytes:
        raise NotImplementedError

    def store(self, data: bytes) -> DataID:
        raise NotImplementedError

    def get_uuid(self, data: bytes) -> DataID:
        return self.store(data)

    def remove(self, h: DataID) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(list(iter(self)))

    def __iter__(self) -> Iterator[DataID]:
        raise NotImplementedError


from .path import DirectoryDataStorage
from .temp import TempDataStorage
from .rds import RemoteDataStorage
