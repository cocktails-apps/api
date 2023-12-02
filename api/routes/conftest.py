from unittest.mock import create_autospec

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..storage import Storage


@pytest.fixture
def app() -> FastAPI:
    return FastAPI(debug=True)


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def storage() -> Storage:
    return create_autospec(Storage, spec_set=True, instance=True)
