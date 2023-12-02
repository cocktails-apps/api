import os
from functools import cache

from motor.motor_asyncio import AsyncIOMotorClient


@cache
def get_client() -> AsyncIOMotorClient:
    # NOTE: MONGODB_URI is a part of Vercel <-> MongoDB integration
    return AsyncIOMotorClient(os.environ["MONGODB_URI"])
