import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from .coctails import Coctails, register_coctails_routes


@pytest.fixture
def app(app: FastAPI) -> FastAPI:
    register_coctails_routes(app)
    return app


def test_health(client: TestClient) -> None:
    resp = client.get("/coctails/?name=screwdriver")
    resp.raise_for_status()

    coctails = TypeAdapter(Coctails).validate_json(resp.text)
    assert len(coctails) == 1
    coctail = coctails[0]
    assert coctail.name == "screwdriver"
    assert coctail.description == "Cool coctail."
