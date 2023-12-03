from unittest.mock import create_autospec

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from ..storage import Glass, GlassWithoutId, Storage
from .glasses import register_glasses_routes


@pytest.fixture
def storage() -> Storage:
    return create_autospec(Storage, spec_set=True, instance=True)


@pytest.fixture
def app(app: FastAPI, storage: Storage) -> FastAPI:
    register_glasses_routes(app, storage)
    return app


def test_get_all(client: TestClient, storage: Storage, glass: Glass) -> None:
    storage.get_glasses.return_value = [glass]

    resp = client.get("/glasses")
    resp.raise_for_status()

    glasses = TypeAdapter(list[Glass]).validate_json(resp.text)
    assert len(glasses) == 1
    assert glasses[0] == glass


async def test_create(client: TestClient, storage: Storage, glass: Glass) -> None:
    glass_without_id = GlassWithoutId.model_validate(glass.model_dump(by_alias=True))
    storage.save_glass.return_value = glass

    resp = client.post("/glasses", json=glass_without_id.model_dump(by_alias=True))
    resp.raise_for_status()

    glass_resp = Glass.model_validate_json(resp.text)
    assert glass_resp == glass
