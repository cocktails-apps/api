import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from . import register_info_routes


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI(debug=True)
    register_info_routes(app)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
