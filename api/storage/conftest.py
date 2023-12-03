import pytest
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase


@pytest.fixture
def mongo_client() -> AsyncMongoMockClient:
    return AsyncMongoMockClient()


@pytest.fixture
def mongo_db(mongo_client: AsyncMongoMockClient) -> AsyncMongoMockDatabase:
    return mongo_client.get_database("test_db")


@pytest.fixture
def document_id() -> str:
    return str(ObjectId())
