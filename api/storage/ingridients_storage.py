from typing import NewType

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .commons import ApiBaseModel, DocumentNotFound, add_metadata

IngridientId = NewType("IngridientId", str)


class IngridientWithoutId(ApiBaseModel):
    name: str
    description: str


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
            id=str(res.inserted_id),
            name=ingridient.name,
            description=ingridient.description,
        )

    async def get_by_id(self, id: IngridientId) -> Ingridient:
        res = await self._collection.find_one({"_id": ObjectId(id)})
        if res is None:
            raise DocumentNotFound(f"Ingridient with {id=} not found")

        res["id"] = str(res["_id"])
        return Ingridient.model_validate(res)
