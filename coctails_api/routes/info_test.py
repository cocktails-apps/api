import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .info import HealthResponse, register_info_routes


@pytest.fixture
def app(app: FastAPI) -> FastAPI:
    register_info_routes(app)
    return app


def test_health(client: TestClient) -> None:
    resp = client.get("/info/health")
    resp.raise_for_status()
    health = HealthResponse.model_validate_json(resp.text)
    assert health.status == "OK"
