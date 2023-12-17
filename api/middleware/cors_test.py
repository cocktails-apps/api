import os
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .cors import CORS_ORIGINS_ENV, register_cors_middleware


@pytest.fixture
def app() -> FastAPI:
    res = FastAPI()

    @res.get("/")
    def _():
        return "test"

    return res


def test_cors_env_one_item(app: FastAPI) -> None:
    with patch.dict(os.environ, {CORS_ORIGINS_ENV: "http://test.com"}, clear=True):
        register_cors_middleware(app)

    client = TestClient(app)

    response = client.options(
        "/",
        headers={
            "Origin": "http://test.com",
        },
    )

    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://test.com"


def test_cors_env_several_item(app: FastAPI) -> None:
    with patch.dict(
        os.environ,
        {CORS_ORIGINS_ENV: "http://test.com, http://localhost:3000"},
        clear=True,
    ):
        register_cors_middleware(app)

    client = TestClient(app)

    response = client.options(
        "/",
        headers={
            "Origin": "http://localhost:3000",
        },
    )

    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_cors_env_not_set(app: FastAPI) -> None:
    with patch.dict(os.environ, clear=True):
        register_cors_middleware(app)

    client = TestClient(app)

    response = client.options(
        "/",
        headers={
            "Origin": "http://test.com",
        },
    )

    assert "access-control-allow-origin" not in response.headers
    assert "access-control-allow-credentials" not in response.headers
