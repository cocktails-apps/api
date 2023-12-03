from typing import NewType

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .commons import ApiBaseModel, DocumentNotFound, add_metadata

GlassId = NewType("GlassId", str)


class GlassWithoutId(ApiBaseModel):
    name: str
    description: str


class Glass(GlassWithoutId):
    id: GlassId


GLASS_COLLECTION = "glasses"


class GlassesStorage:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db[GLASS_COLLECTION]

    async def save(self, glass: GlassWithoutId) -> Glass:
        res = await self._collection.insert_one(
            add_metadata(glass.model_dump(by_alias=True))
        )
        return Glass(
            id=GlassId(str(res.inserted_id)),
            name=glass.name,
            description=glass.description,
        )

    async def get_by_id(self, id: GlassId) -> Glass:
        res = await self._collection.find_one({"_id": ObjectId(id)})
        if res is None:
            raise DocumentNotFound(f"Glass with {id=} not found")

        res = dict(res)
        res["id"] = str(res["_id"])
        return Glass.model_validate(res)
