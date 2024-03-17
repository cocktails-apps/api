import httpx
from typing_extensions import override
from yarl import URL

from ...clients.vercel import blob_upload
from .base import BlobStorage, BlobStorageError


class VercelBlobStorageError(BlobStorageError):
    pass


class VercelBlobStorage(BlobStorage):
    def __init__(self, client: httpx.AsyncClient, folder_prefix: str) -> None:
        super().__init__()
        self._client = client
        self._folder_prefix = folder_prefix

    @override
    async def upload(self, folder: str, file_name: str, data: bytes) -> URL:
        try:
            res = await blob_upload(
                self._client, f"{self._folder_prefix}-{folder}", file_name, data
            )
            return URL(str(res.url))
        except Exception as exc:
            raise VercelBlobStorageError(
                f"failed to upload file '{file_name}' to folder '{folder}'"
            ) from exc


def vercel_blob_storage(client: httpx.AsyncClient, env: str) -> VercelBlobStorage:
    return VercelBlobStorage(client=client, folder_prefix=env)
