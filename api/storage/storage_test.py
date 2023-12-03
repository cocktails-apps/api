from unittest.mock import create_autospec

import pytest
from bson import ObjectId

from .coctails_storage import (
    CoctailGlassPartial,
    CoctailIngridientPartial,
    CoctailPartial,
    CoctailsStorage,
)
from .glasses_storage import Glass, GlassesStorage
from .ingridients_storage import Ingridient, IngridientsStorage
from .storage import Storage


@pytest.fixture
def ingridients_storage() -> IngridientsStorage:
    return create_autospec(IngridientsStorage, spec_set=True, instance=True)


@pytest.fixture
def glass_storage() -> GlassesStorage:
    return create_autospec(GlassesStorage, spec_set=True, instance=True)


@pytest.fixture
def coctails_storage() -> CoctailsStorage:
    return create_autospec(CoctailsStorage, spec_set=True, instance=True)


@pytest.fixture
def ingridient() -> Ingridient:
    return Ingridient(id=str(ObjectId()), name="test ingridient", description="test")


@pytest.fixture
def glass() -> Glass:
    return Glass(id=str(ObjectId()), name="test glass", description="test")


@pytest.fixture
def coctail(ingridient: Ingridient, glass: Glass) -> CoctailPartial:
    return CoctailPartial(
        id=str(ObjectId()),
        name="test coctail",
        description="test",
        ingridients=[CoctailIngridientPartial(id=ingridient.id, amount=150)],
        glasses=[CoctailGlassPartial(id=glass.id)],
    )


@pytest.fixture
def sut(
    ingridients_storage: IngridientsStorage,
    glass_storage: GlassesStorage,
    coctails_storage: CoctailsStorage,
) -> Storage:
    return Storage(ingridients_storage, glass_storage, coctails_storage)


async def test_save_ingridient(
    sut: Storage, ingridients_storage: IngridientsStorage, ingridient: Ingridient
) -> None:
    ingridients_storage.save.return_value = ingridient
    result = await sut.save_ingridient(ingridient)
    assert result == ingridient
    ingridients_storage.save.assert_called_once()


async def test_get_ingridient_by_id(
    sut: Storage, ingridients_storage: IngridientsStorage, ingridient: Ingridient
) -> None:
    ingridients_storage.get_by_id.return_value = ingridient
    result = await sut.get_ingridient_by_id(ingridient.id)
    assert result == ingridient
    ingridients_storage.get_by_id.assert_called_once()


async def test_save_glass(
    sut: Storage, glass_storage: GlassesStorage, glass: Glass
) -> None:
    glass_storage.save.return_value = glass
    result = await sut.save_glass(glass)
    assert result == glass
    glass_storage.save.assert_called_once()


async def test_get_glass_by_id(
    sut: Storage, glass_storage: GlassesStorage, glass: Glass
) -> None:
    glass_storage.get_by_id.return_value = glass
    result = await sut.get_glass_by_id(glass.id)
    assert result == glass
    glass_storage.get_by_id.assert_called_once()


async def test_get_glasses(
    sut: Storage, glass_storage: GlassesStorage, glass: Glass
) -> None:
    glass_storage.get_all.return_value = [glass]
    assert await sut.get_glasses() == [glass]
    glass_storage.get_all.assert_called_once()


async def test_save_coctail(
    sut: Storage,
    ingridients_storage: IngridientsStorage,
    glass_storage: GlassesStorage,
    coctails_storage: CoctailsStorage,
    ingridient: Ingridient,
    glass: Glass,
    coctail: CoctailPartial,
) -> None:
    ingridients_storage.get_by_id.return_value = ingridient
    glass_storage.get_by_id.return_value = glass
    coctails_storage.get_by_id.return_value = coctail
    coctails_storage.save.return_value = coctail

    result = await sut.save_coctail(coctail)

    assert result.id == coctail.id
    assert result.name == coctail.name
    assert result.description == coctail.description
    assert len(result.ingridients) == len(coctail.ingridients)
    assert len(result.glasses) == len(coctail.glasses)
    coctails_storage.save.assert_called_once()


async def test_get_coctail_by_id(
    sut: Storage,
    ingridients_storage: IngridientsStorage,
    glass_storage: GlassesStorage,
    coctails_storage: CoctailsStorage,
    ingridient: Ingridient,
    glass: Glass,
    coctail: CoctailPartial,
) -> None:
    ingridients_storage.get_by_id.return_value = ingridient
    glass_storage.get_by_id.return_value = glass
    coctails_storage.get_by_id.return_value = coctail

    result = await sut.get_coctail_by_id(coctail.id)

    assert result.id == coctail.id
    assert result.name == coctail.name
    assert result.description == coctail.description
    assert len(result.ingridients) == len(coctail.ingridients)
    assert len(result.glasses) == len(coctail.glasses)
    coctails_storage.get_by_id.assert_called_once()
