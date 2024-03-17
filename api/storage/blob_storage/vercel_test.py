from collections.abc import Iterable
from unittest.mock import MagicMock, create_autospec, patch

import httpx
import pytest
from yarl import URL

from ...clients.vercel import BlobUploadResult
from .vercel import VercelBlobStorage, VercelBlobStorageError


@pytest.fixture
def client() -> httpx.AsyncClient:
    return create_autospec(httpx.AsyncClient, spec_set=True, instance=True)


@pytest.fixture
def mock_blob_upload() -> Iterable[MagicMock]:
    with patch("api.storage.blob_storage.vercel.blob_upload") as mock:
        yield mock


@pytest.fixture
def sut(client: httpx.AsyncClient) -> VercelBlobStorage:
    return VercelBlobStorage(client=client)


async def test_upload(sut: VercelBlobStorage, mock_blob_upload: MagicMock):
    folder = "folder"
    file_name = "file_name"
    data = b"data"

    mock_blob_upload.return_value = BlobUploadResult(url="https://example.com")

    result = await sut.upload(folder, file_name, data)

    assert result == URL("https://example.com")
    mock_blob_upload.assert_called_once_with(sut._client, folder, file_name, data)


async def test_upload_failure(sut: VercelBlobStorage, mock_blob_upload: MagicMock):
    folder = "folder"
    file_name = "file_name"
    data = b"data"

    mock_blob_upload.side_effect = Exception("error")

    with pytest.raises(VercelBlobStorageError, match="failed to upload file"):
        await sut.upload(folder, file_name, data)

    mock_blob_upload.assert_called_once_with(sut._client, folder, file_name, data)
