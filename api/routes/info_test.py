import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..storage import Storage
from .info import HealthResponse, register_info_routes


@pytest.fixture
def app(app: FastAPI, storage: Storage) -> FastAPI:
    register_info_routes(app, storage)
    return app


def test_health_ok(client: TestClient, storage: Storage) -> None:
    storage.is_connected.return_value = True

    resp = client.get("/info/health")
    resp.raise_for_status()
    health = HealthResponse.model_validate_json(resp.text)
    assert health.status == "OK"


def test_health_mongo_not_connected(client: TestClient, storage: Storage) -> None:
    storage.is_connected.return_value = False

    resp = client.get("/info/health")
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Not connected to MongoDB"}
