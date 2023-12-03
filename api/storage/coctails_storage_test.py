import pytest
from bson import ObjectId
from mongomock_motor import AsyncMongoMockDatabase

from .coctails_storage import (
    CoctailGlassPartial,
    CoctailIngridientPartial,
    CoctailPartial,
    CoctailsStorage,
)
from .commons import DocumentNotFound


@pytest.fixture
def sut(mongo_db: AsyncMongoMockDatabase) -> CoctailsStorage:
    return CoctailsStorage(mongo_db)


@pytest.fixture
def coctail_partial() -> CoctailPartial:
    return CoctailPartial(
        id=str(ObjectId()),
        name="test coctail",
        description="test",
        ingridients={CoctailIngridientPartial(id=str(ObjectId()), amount=150)},
        glasses={CoctailGlassPartial(id=str(ObjectId()))},
    )


async def test_get_by_id_not_found(sut: CoctailsStorage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_by_id(document_id)


async def test_save_get(sut: CoctailsStorage, coctail_partial: CoctailPartial):
    coctail = await sut.save(coctail_partial)
    assert coctail == await sut.get_by_id(coctail.id)


async def test_get_all(sut: CoctailsStorage, coctail_partial: CoctailPartial):
    coctail = await sut.save(coctail_partial)
    assert [coctail] == await sut.get_all()
