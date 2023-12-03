import pytest
from mongomock_motor import AsyncMongoMockDatabase

from .commons import DocumentNotFound
from .glass_storage import GlassStorage, GlassWithoutId


@pytest.fixture
def sut(mongo_db: AsyncMongoMockDatabase) -> GlassStorage:
    return GlassStorage(mongo_db)


async def test_get_by_id_not_found(sut: GlassStorage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_by_id(document_id)


async def test_save_get(sut: GlassStorage):
    upload = GlassWithoutId(name="test name", description="test description")
    glass = await sut.save(upload)

    assert glass == await sut.get_by_id(glass.id)
