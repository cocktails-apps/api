from unittest.mock import create_autospec

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from ..storage import Ingridient, IngridientWithoutId, Storage
from .ingridients import register_ingridients_routes


@pytest.fixture
def storage() -> Storage:
    return create_autospec(Storage, spec_set=True, instance=True)


@pytest.fixture
def app(app: FastAPI, storage: Storage) -> FastAPI:
    register_ingridients_routes(app, storage)
    return app


def test_get_all(client: TestClient, storage: Storage, ingridient: Ingridient) -> None:
    storage.get_ingridients.return_value = [ingridient]

    resp = client.get("/ingridients")
    resp.raise_for_status()

    ingridients = TypeAdapter(list[Ingridient]).validate_json(resp.text)
    assert len(ingridients) == 1
    ingridient_resp = ingridients[0]
    assert ingridient_resp == ingridient


async def test_create(
    client: TestClient, storage: Storage, ingridient: Ingridient
) -> None:
    ingridient_without_id = IngridientWithoutId.model_validate(
        ingridient.model_dump(by_alias=True)
    )
    storage.save_ingridient.return_value = ingridient

    resp = client.post(
        "/ingridients", json=ingridient_without_id.model_dump(by_alias=True)
    )
    resp.raise_for_status()

    ingridient_resp = Ingridient.model_validate_json(resp.text)
    assert ingridient_resp == ingridient
