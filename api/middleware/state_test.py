from unittest.mock import create_autospec

import httpx
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from ..storage import BlobStorage
from .state import blob_storage_from_request, http_client_from_request


@pytest.fixture
def http_client() -> httpx.AsyncClient:
    return create_autospec(httpx.AsyncClient, spec_set=True, instance=True)


@pytest.fixture
def blob_storage() -> BlobStorage:
    return create_autospec(BlobStorage, spec_set=True, instance=True)


@pytest.fixture
def app(http_client: httpx.AsyncClient, blob_storage: BlobStorage) -> FastAPI:
    app = FastAPI()

    @app.middleware("http")
    async def _(request: Request, call_next):
        request.state.http_client = http_client
        request.state.blob_storage = blob_storage
        return await call_next(request)

    return app


def test_route_context(
    app: FastAPI, http_client: httpx.AsyncClient, blob_storage: BlobStorage
):
    @app.get("/")
    def handler(request: Request) -> None:
        assert http_client_from_request(request) is http_client
        assert blob_storage_from_request(request) is blob_storage

    with TestClient(app) as client:
        client.get("/")
