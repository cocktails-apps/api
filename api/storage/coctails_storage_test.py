import pytest
from bson import ObjectId
from mongomock_motor import AsyncMongoMockDatabase

from .coctails_storage import (
    CoctailGlassPartial,
    CoctailIngridientPartial,
    CoctailPartialWithoutId,
    CoctailsStorage,
)
from .commons import DocumentNotFound


@pytest.fixture
def sut(mongo_db: AsyncMongoMockDatabase) -> CoctailsStorage:
    return CoctailsStorage(mongo_db)


async def test_get_by_id_not_found(sut: CoctailsStorage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_by_id(document_id)


async def test_save_get(sut: CoctailsStorage):
    upload = CoctailPartialWithoutId(
        name="test name",
        description="test description",
        ingridients=set([
            CoctailIngridientPartial(id=str(ObjectId()), amount=50),
            CoctailIngridientPartial(id=str(ObjectId()), amount=100),
        ]),
        glasses=set([
            CoctailGlassPartial(id=str(ObjectId())),
            CoctailGlassPartial(id=str(ObjectId())),
        ]),
    )
    coctail = await sut.save(upload)

    assert coctail == await sut.get_by_id(coctail.id)
