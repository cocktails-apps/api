from unittest.mock import AsyncMock, create_autospec

import pytest
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient

from .models import (
    CoctailGlassUpload,
    CoctailIngridientUpload,
    CoctailUpload,
    GlassUpload,
    IngridientUpload,
)
from .storage import DocumentNotFound, Storage


@pytest.fixture
def mongo_client() -> AsyncMongoMockClient:
    return AsyncMongoMockClient()


@pytest.fixture
def sut(mongo_client: AsyncMongoMockClient) -> Storage:
    return Storage(mongo_client)


@pytest.fixture
def document_id() -> str:
    return str(ObjectId())


async def test_is_connected():
    mongo_client = create_autospec(AsyncIOMotorClient, spec_set=True, instance=True)
    mongo_client.server_info = AsyncMock(return_value={})
    sut = Storage(mongo_client)

    assert await sut.is_connected()

    mongo_client.server_info.side_effect = Exception()
    assert not await sut.is_connected()


async def test_get_ingridient_by_id_not_found(sut: Storage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_ingridient_by_id(document_id)


async def test_save_get_ingridient(sut: Storage):
    upload = IngridientUpload(name="test name", description="test description")
    ingridient = await sut.save_ingridient(upload)

    assert ingridient == await sut.get_ingridient_by_id(ingridient.id)


async def test_get_glass_by_id_not_found(sut: Storage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_glass_by_id(document_id)


async def test_save_get_glass(sut: Storage):
    upload = GlassUpload(name="test name", description="test description")
    glass = await sut.save_glass(upload)

    assert glass == await sut.get_glass_by_id(glass.id)


async def test_get_coctail_by_id_not_found(sut: Storage, document_id: str):
    with pytest.raises(DocumentNotFound):
        await sut.get_coctail_by_id(document_id)


async def test_save_get_coctail(sut: Storage):
    ingridient = await sut.save_ingridient(
        IngridientUpload(name="test name", description="test description")
    )
    glass = await sut.save_glass(
        GlassUpload(name="test name", description="test description")
    )

    upload = CoctailUpload(
        name="test name",
        description="test description",
        ingredients=[CoctailIngridientUpload(id=ingridient.id)],
        glass_type=[CoctailGlassUpload(id=glass.id)],
    )
    coctail = await sut.save_coctail(upload)

    assert coctail == await sut.get_coctail_by_id(coctail.id)


async def test_save_coctail_with_missing_ingridient(sut: Storage, document_id: str):
    glass = await sut.save_glass(
        GlassUpload(name="test name", description="test description")
    )

    upload = CoctailUpload(
        name="test name",
        description="test description",
        ingredients=[CoctailIngridientUpload(id=document_id)],
        glass_type=[CoctailGlassUpload(id=glass.id)],
    )
    with pytest.raises(DocumentNotFound):
        await sut.save_coctail(upload)


async def test_save_coctail_with_missing_glass(sut: Storage, document_id: str):
    ingridient = await sut.save_ingridient(
        IngridientUpload(name="test name", description="test description")
    )

    upload = CoctailUpload(
        name="test name",
        description="test description",
        ingredients=[CoctailIngridientUpload(id=ingridient.id)],
        glass_type=[CoctailGlassUpload(id=document_id)],
    )
    with pytest.raises(DocumentNotFound):
        await sut.save_coctail(upload)
