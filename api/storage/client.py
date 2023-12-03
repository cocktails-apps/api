import os
from functools import cache

from motor.motor_asyncio import AsyncIOMotorClient


@cache
def get_client() -> AsyncIOMotorClient:
    # NOTE: MONGODB_URI is a part of Vercel <-> MongoDB integration
    return AsyncIOMotorClient(os.environ["MONGODB_URI"])


async def is_connected(mongo_client: AsyncIOMotorClient | None = None) -> bool:
    if mongo_client is None:
        mongo_client = get_client()

    try:
        await mongo_client.server_info()
        return True
    except Exception:
        return False
