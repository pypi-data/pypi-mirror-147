import os
from dataclasses import dataclass
from enum import Enum
from hashlib import md5, sha256
from pathlib import Path
from typing import Iterator, Optional, Union, Any, Tuple
import requests
from requests.auth import HTTPBasicAuth

from . import DataStorage, DataID

from pydantic import PrivateAttr

REMOTE_DATA_STORAGE_SERVER_HEALTH_CHECK_DATA = {"data": "RemoteDataStorage", "error": None, "success": True}

@dataclass
class RemoteDataStorageServer:
    url: str

    def is_valid(self) -> bool:
        res = requests.get(self.url)
        if not res.ok:
            return False
        res_eq: bool = res.json() == REMOTE_DATA_STORAGE_SERVER_HEALTH_CHECK_DATA
        return res_eq

    def get_account(self, username: str, password: str) -> "RemoteDataStorageAccount":
        account = RemoteDataStorageAccount(self.url, username, password)
        if not account.is_valid():
            raise Exception(f"invalid rds account {account.username}@{account.url}")
        return account

@dataclass
class RemoteDataStorageAccount:
    url: str
    username: str
    password: str

    @property
    def server(self) -> RemoteDataStorageServer:
        return RemoteDataStorageServer(self.url)

    @server.setter
    def server(self, value: RemoteDataStorageServer) -> None:
        self.url = value.url

    def is_valid(self) -> bool:
        if self.server.is_valid():
            res = requests.get(f"{self.url}/pools/", auth=HTTPBasicAuth(self.username, self.password))
            return res.ok and res.json()["success"]
        return False

    def create_pool(self) -> "RemoteDataStorage":
        assert self.is_valid()
        res = requests.post(f"{self.url}/pools/", auth=HTTPBasicAuth(self.username, self.password))
        assert res.ok
        jres = res.json()
        assert jres["success"]
        rds = RemoteDataStorage(self.url, jres["data"]["token"])
        rds._pool = jres["data"]["uuid"]
        return rds


def is_valid_url(url: str) -> bool:
    res = requests.get(url)
    if not res.ok:
        return False
    res_eq: bool = res.json() == {"data": "RemoteDataStorage", "error": None, "success": True}
    return res_eq

class AccessType(Enum):
    FULL = "full"
    WRITE = "write"
    READ = "read"

class RemoteDataStorage(DataStorage):
    muuid = "e9be7b8b-5cf4-4931-a9e8-966138822e05"
    url: str
    token: str
    _pool: Optional[str] = PrivateAttr(None)
    _session: Optional[requests.Session] = PrivateAttr(None)
    _level: Optional[AccessType] = PrivateAttr(None)

    def destroy(self) -> bool:
        if self.level != AccessType.FULL:
            return False
        res = self.session.delete(f"{self.url}/pools/{self.pool}")
        if not res.ok:
            return False
        jres = res.json()
        return jres["success"] is True

    def __init__(self, url: str, token: str):
        super().__init__(url=url, token=token)

    @property
    def level(self) -> AccessType:
        if self._level is None:
            res = self.session.get(f"{self.url}/token/{self.token}")
            assert res.ok
            jres = res.json()
            assert jres["success"]
            self._level = {t.value: t for t in AccessType}[jres["data"]["type"]]
        return self._level

    @classmethod
    def from_user(cls, url: str, username: str, password: str) -> "RemoteDataStorage":
        return RemoteDataStorageServer(url).get_account(username, password).create_pool()

    @property
    def server(self) -> RemoteDataStorageServer:
        return RemoteDataStorageServer(self.url)

    def is_valid(self) -> bool:
        if self.server.is_valid():
            try:
                self._level = None
                self.level
            except AssertionError:
                return False
            return True
        return False

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._session.headers["Authorization"] = f"Bearer {self.token}"
        return self._session

    @property
    def pool(self) -> str:
        assert self.is_valid()
        if self._pool is None:
            res = self.session.get(f"{self.url}/pools/")
            assert res.ok
            jres = res.json()
            assert jres["success"]
            self._pool = jres["data"][0]["uuid"]
        return self._pool

    def has(self, h: Optional[DataID]) -> bool:
        res = self.session.head(f"{self.url}/data/{h}")
        return res.ok

    def get(self, h: DataID) -> bytes:
        res = self.session.get(f"{self.url}/data/{h}")
        assert res.ok
        return res.content

    def store(self, data: bytes) -> DataID:
        res = self.session.post(f"{self.url}/data/")
        assert res.ok
        jres = res.json()
        assert jres["success"]
        id_ = jres["data"]["uuid"]
        res = self.session.put(f"{self.url}/data/{id_}", data=data)
        assert res.ok
        jres = res.json()
        assert jres["success"]
        return DataID(jres["data"]["uuid"])

    def remove(self, h: DataID) -> bool:
        res = self.session.delete(f"{self.url}/data/{h}")
        if not res.ok:
            return False
        jres = res.json()
        return jres["success"] is True

    def __iter__(self) -> Iterator[DataID]:
        res = self.session.get(f"{self.url}/data/")
        assert res.ok
        jres = res.json()
        assert jres["success"]
        return iter(list(d["uuid"] for d in jres["data"]))

