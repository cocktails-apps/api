import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..storage import Coctail, Glass, Ingridient
from ..storage.storage import CoctailIngridient


@pytest.fixture
def app() -> FastAPI:
    return FastAPI(debug=True)


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
