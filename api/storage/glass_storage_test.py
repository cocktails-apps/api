import pytest
from mongomock_motor import AsyncMongoMockDatabase

from .commons import DocumentNotFound
from .glasses_storage import GlassesStorage, GlassWithoutId


@pytest.fixture
def sut(mongo_db: AsyncMongoMockDatabase) -> GlassesStorage:
    return GlassesStorage(mongo_db)


async def test_get_by_id_not_found(sut: GlassesStorage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_by_id(document_id)


async def test_save_get(sut: GlassesStorage):
    upload = GlassWithoutId(name="test name", description="test description")
    glass = await sut.save(upload)

    assert glass == await sut.get_by_id(glass.id)
