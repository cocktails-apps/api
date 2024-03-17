from abc import ABC, abstractmethod

from yarl import URL


class BlobStorageError(Exception):
    pass


class BlobStorage(ABC):
    @abstractmethod
    async def upload(self, folder: str, file_name: str, data: bytes) -> URL: ...
