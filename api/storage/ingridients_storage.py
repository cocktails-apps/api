from typing import Any, Mapping, NewType

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .commons import ApiBaseModel, Description, DocumentNotFound, Name, add_metadata

IngridientId = NewType("IngridientId", str)


class IngridientWithoutId(ApiBaseModel):
    name: Name
    description: Description


class Ingridient(IngridientWithoutId):
    id: IngridientId


INGRIDIENTS_COLLECTION = "ingridients"


class IngridientsStorage:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db[INGRIDIENTS_COLLECTION]

    async def save(self, ingridient: IngridientWithoutId) -> Ingridient:
        res = await self._collection.insert_one(
            add_metadata(ingridient.model_dump(by_alias=True))
        )
        return Ingridient(
            id=IngridientId(str(res.inserted_id)),
            name=ingridient.name,
            description=ingridient.description,
        )

    async def get_by_id(self, ingridient_id: IngridientId) -> Ingridient:
        res = await self._collection.find_one({"_id": ObjectId(ingridient_id)})
        if res is None:
            raise DocumentNotFound(f"Ingridient with id={ingridient_id} not found")

        return self._parse_doc(res)

    async def get_all(self) -> list[Ingridient]:
        cur = self._collection.find()
        return list(map(self._parse_doc, await cur.to_list(length=None)))

    @staticmethod
    def _parse_doc(doc: Mapping[str, Any]) -> Ingridient:
        doc = dict(doc)
        doc["id"] = str(doc["_id"])
        return Ingridient.model_validate(doc)
