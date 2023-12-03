from collections.abc import Mapping
from typing import Any, NewType

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .commons import ApiBaseModel, Description, DocumentNotFound, Name, add_metadata

GlassId = NewType("GlassId", str)


class GlassWithoutId(ApiBaseModel):
    name: Name
    description: Description


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

        return self._parse_doc(res)

    async def get_all(self) -> list[Glass]:
        cur = self._collection.find()
        return list(map(self._parse_doc, await cur.to_list(length=None)))

    @staticmethod
    def _parse_doc(doc: Mapping[str, Any]) -> Glass:
        doc = dict(doc)
        doc["id"] = str(doc["_id"])
        return Glass.model_validate(doc)
