from unittest.mock import AsyncMock, create_autospec

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from .info import HealthResponse, register_info_routes


@pytest.fixture
def mongo_client() -> AsyncIOMotorClient:
    m = create_autospec(AsyncIOMotorClient, spec_set=True, instance=True)
    m.server_info = AsyncMock()
    return m


@pytest.fixture
def app(app: FastAPI, mongo_client: AsyncIOMotorClient) -> FastAPI:
    register_info_routes(app, mongo_client)
    return app


def test_health_ok(client: TestClient, mongo_client: AsyncIOMotorClient) -> None:
    mongo_client.server_info.return_value = {}

    resp = client.get("/info/health")
    resp.raise_for_status()
    health = HealthResponse.model_validate_json(resp.text)
    assert health.status == "OK"


def test_health_mongo_not_connected(
    client: TestClient, mongo_client: AsyncIOMotorClient
) -> None:
    mongo_client.server_info.side_effect = Exception("Not connected")

    resp = client.get("/info/health")
    assert resp.status_code == 500
    assert resp.json() == {"detail": "Not connected to MongoDB"}
