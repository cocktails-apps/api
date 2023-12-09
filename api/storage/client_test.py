from unittest.mock import AsyncMock, create_autospec

import pymongo.errors
from motor.motor_asyncio import AsyncIOMotorClient

from .client import is_connected


async def test_is_connected():
    mongo_client = create_autospec(AsyncIOMotorClient, spec_set=True, instance=True)
    mongo_client.server_info = AsyncMock(return_value={})

    assert await is_connected(mongo_client)

    mongo_client.server_info.side_effect = pymongo.errors.ServerSelectionTimeoutError
    assert not await is_connected(mongo_client)
