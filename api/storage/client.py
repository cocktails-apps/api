import os
from functools import cache
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient


@cache
def get_client() -> AsyncIOMotorClient:
    if os.environ.get("USE_MONGOMOCK", False):
        from mongomock_motor import AsyncMongoMockClient  # type: ignore[import-untyped]

        return AsyncMongoMockClient()  # type: ignore[no-any-return]

    # NOTE: MONGODB_URI is a part of Vercel <-> MongoDB integration
    return AsyncIOMotorClient(os.environ["MONGODB_URI"])


async def is_connected(mongo_client: Optional[AsyncIOMotorClient] = None) -> bool:
    if mongo_client is None:
        mongo_client = get_client()

    try:
        await mongo_client.server_info()
        return True
    except Exception:
        return False
