from http import HTTPStatus
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from ..storage import Coctail, CoctailPartialWithoutId, DocumentNotFound, Storage
from .coctails import register_coctails_routes


@pytest.fixture
def app(app: FastAPI, storage: Storage) -> FastAPI:
    register_coctails_routes(app)
    with patch("api.routes.coctails.get_storage", return_value=storage):
        yield app


def test_get_all(client: TestClient, storage: Storage, coctail: Coctail) -> None:
    storage.get_coctails.return_value = [coctail]

    resp = client.get("/coctails")
    resp.raise_for_status()

    coctails = TypeAdapter(list[Coctail]).validate_json(resp.text)
    assert len(coctails) == 1
    assert coctails[0] == coctail


async def test_create(client: TestClient, storage: Storage, coctail: Coctail) -> None:
    coctail_partial_without_id = CoctailPartialWithoutId.model_validate(
        coctail.model_dump(by_alias=True, mode="json")
    )
    storage.save_coctail.return_value = coctail

    resp = client.post(
        "/coctails",
        json=coctail_partial_without_id.model_dump(by_alias=True, mode="json"),
    )
    resp.raise_for_status()

    coctail_resp = Coctail.model_validate_json(resp.text)
    assert coctail_resp == coctail


async def test_create_not_found(
    app: FastAPI, storage: Storage, coctail: Coctail
) -> None:
    client = TestClient(app, raise_server_exceptions=False)
    coctail_partial_without_id = CoctailPartialWithoutId.model_validate(
        coctail.model_dump(by_alias=True, mode="json")
    )
    storage.save_coctail.side_effect = DocumentNotFound("Ingridient not found")

    resp = client.post(
        "/coctails",
        json=coctail_partial_without_id.model_dump(by_alias=True, mode="json"),
    )
    assert resp.status_code == HTTPStatus.NOT_FOUND
