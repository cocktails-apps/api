from motor.motor_asyncio import AsyncIOMotorClient

from .models import Coctail, CoctailDocument, GlassDocument, IngridientDocument

DB_NAME = "coctails"


class Storage:
    def __init__(self, mongo_client: AsyncIOMotorClient) -> None:
        self._mongo_client = mongo_client
        self._db = mongo_client[DB_NAME]
        self._ingridients = self._db[IngridientDocument.collection_name]
        self._glasses = self._db[GlassDocument.collection_name]
        self._coctails = self._db[CoctailDocument.collection_name]

    async def is_connected(self) -> bool:
        try:
            await self._mongo_client.server_info()
            return True
        except Exception:
            return False

    async def get_coctails(self) -> list[Coctail]:
        return [
            Coctail(
                name="screwdriver",
                description="Cool coctail",
                ingredients=[],
                glass_type=[],
            )
        ]
