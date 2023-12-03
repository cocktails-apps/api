import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    return FastAPI(debug=True)


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
