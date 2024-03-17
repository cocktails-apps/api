from typing import Optional
from unittest.mock import create_autospec, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from yarl import URL

from ..middleware import blob_storage_from_request
from ..storage import BlobStorage
from .file_storage import _is_image, register_file_storage_routes


@pytest.fixture
def blob_storage() -> BlobStorage:
    res = create_autospec(BlobStorage, spec_set=True, instance=True)
    with patch(
        "api.routes.file_storage.blob_storage_from_request",
        spec_set=blob_storage_from_request,
        return_value=res,
    ):
        yield res


@pytest.fixture
def app(app: FastAPI) -> FastAPI:
    register_file_storage_routes(app)
    return app


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


async def test_upload(client: TestClient, blob_storage: BlobStorage) -> None:
    blob_storage.upload.return_value = URL("https://some.url/ingridient/file.png")

    resp = client.post(
        "/files",
        data={"category": "ingridient"},
        files={"file": ("file.png", b"some data")},
    )

    assert resp.text == "https://some.url/ingridient/file.png"
    blob_storage.upload.assert_awaited_once()


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
