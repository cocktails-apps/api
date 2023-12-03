from unittest.mock import create_autospec, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..storage import Coctail, Glass, Ingridient, Storage
from ..storage.storage import CoctailIngridient


@pytest.fixture
def storage() -> Storage:
    return create_autospec(Storage, spec_set=True, instance=True)


@pytest.fixture
def app(storage: Storage) -> FastAPI:
    with patch("api.routes.coctails.get_storage", return_value=storage), patch(
        "api.routes.glasses.get_storage", return_value=storage
    ), patch("api.routes.ingridients.get_storage", return_value=storage):
        yield FastAPI(debug=True)


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def glass() -> Glass:
    return Glass(id="1", name="highball", description="Some description")


@pytest.fixture
def ingridient() -> Ingridient:
    return Ingridient(id="1", name="Orange juice", description="Some description")


@pytest.fixture
def coctail(ingridient: Ingridient, glass: Glass) -> Coctail:
    coctail_ingridient = CoctailIngridient(
        **ingridient.model_dump(by_alias=True), amount=150
    )
    return Coctail(
        id="1",
        name="screwdriver",
        description="Cool coctail",
        ingridients=[coctail_ingridient],
        glasses=[glass],
    )
