from typing import NewType

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from .commons import ApiBaseModel, DocumentNotFound, add_metadata
from .glass_storage import GlassId
from .ingridients_storage import IngridientId

CoctailId = NewType("CoctailId", str)


class CoctailIngridientPartial(ApiBaseModel):
    id: IngridientId
    amount: int


class CoctailGlassPartial(ApiBaseModel):
    id: GlassId


class CoctailPartialWithoutId(ApiBaseModel):
    name: str
    description: str
    ingridients: list[CoctailIngridientPartial]
    glass: list[CoctailGlassPartial]


class CoctailPartial(CoctailPartialWithoutId):
    id: CoctailId


COCTAILS_COLLECTION = "coctails"


class CoctailsStorage:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db[COCTAILS_COLLECTION]

    async def save(self, coctail: CoctailPartialWithoutId) -> CoctailPartial:
        doc = coctail.model_dump(by_alias=True)

        for ing in doc["ingridients"]:
            ing["id"] = ObjectId(ing["id"])
        for glass in doc["glass"]:
            glass["id"] = ObjectId(glass["id"])

        res = await self._collection.insert_one(add_metadata(doc))
        return CoctailPartial(
            id=str(res.inserted_id),
            name=coctail.name,
            description=coctail.description,
            ingridients=coctail.ingridients,
            glass=coctail.glass,
        )

    async def get_by_id(self, id: CoctailId) -> CoctailPartial:
        res = await self._collection.find_one({"_id": ObjectId(id)})
        if res is None:
            raise DocumentNotFound(f"Coctail with {id=} not found")

        res["id"] = str(res["_id"])
        res["ingridients"] = [
            dict(id=str(ingridient["id"]), amount=ingridient["amount"])
            for ingridient in res["ingridients"]
        ]
        res["glass"] = [dict(id=str(glass["id"])) for glass in res["glass"]]
        return CoctailPartial.model_validate(res)
