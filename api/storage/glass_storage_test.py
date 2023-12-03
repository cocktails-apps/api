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


async def test_get_all(sut: GlassesStorage):
    upload = [
        GlassWithoutId(name="glass 1", description="test description"),
        GlassWithoutId(name="glass 2", description="test description"),
    ]

    glasses = [await sut.save(glass) for glass in upload]
    assert glasses == await sut.get_all()
