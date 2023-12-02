import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from ..storage import Coctail, Storage
from .coctails import register_coctails_routes


@pytest.fixture
def app(app: FastAPI, storage: Storage) -> FastAPI:
    register_coctails_routes(app, storage)
    return app


def test_get(client: TestClient, storage: Storage) -> None:
    storage.get_coctails.return_value = [
        Coctail(
            id="1",
            name="screwdriver",
            description="Cool coctail",
            ingredients=[],
            glass_type=[],
        )
    ]

    resp = client.get("/coctails/?name=screwdriver")
    resp.raise_for_status()

    coctails = TypeAdapter(list[Coctail]).validate_json(resp.text)
    assert len(coctails) == 1
    coctail = coctails[0]
    assert coctail.name == "screwdriver"
    assert coctail.description == "Cool coctail"
