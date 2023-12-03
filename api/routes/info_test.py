from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .info import HealthResponse, register_info_routes


@pytest.fixture
def app(app: FastAPI) -> FastAPI:
    register_info_routes(app)
    return app


@pytest.fixture
def mock_is_connected() -> AsyncMock:
    with patch("api.routes.info.is_connected") as mock:
        yield mock


def test_health_ok(client: TestClient, mock_is_connected: AsyncMock) -> None:
    mock_is_connected.return_value = True

    resp = client.get("/info/health")
    resp.raise_for_status()
    health = HealthResponse.model_validate_json(resp.text)
    assert health.status == "OK"


def test_health_mongo_not_connected(
    client: TestClient, mock_is_connected: AsyncMock
) -> None:
    mock_is_connected.return_value = False

    resp = client.get("/info/health")
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Not connected to MongoDB"}
