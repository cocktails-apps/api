from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from unittest.mock import create_autospec

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from .state import State, blob_storage_from_request
from .storage import BlobStorage


@pytest.fixture
def blob_storage() -> BlobStorage:
    return create_autospec(BlobStorage, spec_set=True, instance=True)


@pytest.fixture
def app(blob_storage: BlobStorage) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[State]:
        yield {"blob_storage": blob_storage}

    return FastAPI(lifespan=lifespan)


def test_route_context(app: FastAPI, blob_storage: BlobStorage):
    @app.get("/")
    def handler(request: Request) -> None:
        assert blob_storage_from_request(request) is blob_storage

    with TestClient(app) as client:
        client.get("/")
