from typing import Optional
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..clients.vercel import BlobUploadResult
from ..clients.vercel import blob_upload as blob_upload_orig
from .file_storage import _is_image, register_file_storage_routes


@pytest.fixture
def app(app: FastAPI) -> FastAPI:
    register_file_storage_routes(app)
    return app


@pytest.fixture
def blob_upload() -> AsyncMock:
    with patch(
        "api.routes.file_storage.blob_upload",
        spec_set=blob_upload_orig,
        return_value=BlobUploadResult(url="https://some.url"),
    ) as m:
        yield m


@pytest.mark.parametrize(
    ("file_name", "expected"),
    [
        (None, False),
        ("", False),
        ("file.txt", False),
        ("file.png", True),
    ],
)
def test_is_image(file_name: Optional[str], expected: bool) -> None:
    assert _is_image(file_name) is expected


async def test_upload(client: TestClient, blob_upload: AsyncMock) -> None:
    resp = client.post(
        "/files",
        data={"category": "ingridient"},
        files={"file": ("file.png", b"some data")},
    )

    assert resp.json() == {"url": "https://some.url/"}
    blob_upload.assert_awaited_once()


async def test_upload_not_image_fail(client: TestClient) -> None:
    resp = client.post(
        "/files",
        data={"category": "ingridient"},
        files={"file": ("file.txt", b"some data")},
    )
    assert resp.status_code == 422
    assert resp.json() == {"detail": "File is not an image"}


async def test_upload_wrong_category_fail(client: TestClient) -> None:
    resp = client.post(
        "/files",
        data={"category": "some-category"},
        files={"file": ("file.png", b"some data")},
    )
    assert resp.status_code == 422
    details = resp.json()["detail"]
    assert len(details) == 1
    detail = resp.json()["detail"][0]
    assert "ctx" in detail
    assert detail["ctx"] == {"expected": "'ingridient', 'glass' or 'coctail'"}
    assert "loc" in detail
    assert detail["loc"] == ["body", "category"]
