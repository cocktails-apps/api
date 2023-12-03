import pytest
from mongomock_motor import AsyncMongoMockDatabase

from .commons import DocumentNotFound
from .ingridients_storage import IngridientsStorage, IngridientWithoutId


@pytest.fixture
def sut(mongo_db: AsyncMongoMockDatabase) -> IngridientsStorage:
    return IngridientsStorage(mongo_db)


async def test_get_by_id_not_found(sut: IngridientsStorage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_by_id(document_id)


async def test_save_get(sut: IngridientsStorage):
    upload = IngridientWithoutId(name="test name", description="test description")
    ingridient = await sut.save(upload)

    assert ingridient == await sut.get_by_id(ingridient.id)


async def test_get_all(sut: IngridientsStorage):
    upload = [
        IngridientWithoutId(name="ing 1", description="test description"),
        IngridientWithoutId(name="ing 2", description="test description"),
    ]

    ingridients = [await sut.save(ingridient) for ingridient in upload]
    assert ingridients == await sut.get_all()
