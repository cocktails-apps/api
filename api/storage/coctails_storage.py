from typing import Annotated, Any, Mapping, NewType

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic.types import confrozenset

from .commons import ApiBaseModel, Description, DocumentNotFound, Name, add_metadata
from .glasses_storage import GlassId
from .ingridients_storage import IngridientId

CoctailId = NewType("CoctailId", str)


class CoctailIngridientPartial(ApiBaseModel):
    id: IngridientId
    amount: int


class CoctailGlassPartial(ApiBaseModel):
    id: GlassId


class CoctailPartialWithoutId(ApiBaseModel):
    name: Name
    description: Description
    ingridients: Annotated[
        frozenset[CoctailIngridientPartial],
        confrozenset(CoctailIngridientPartial, min_length=1),
    ]
    glasses: Annotated[
        frozenset[CoctailGlassPartial], confrozenset(CoctailGlassPartial, min_length=1)
    ]


class CoctailPartial(CoctailPartialWithoutId):
    id: CoctailId


COCTAILS_COLLECTION = "coctails"


class CoctailsStorage:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db[COCTAILS_COLLECTION]

    async def save(self, coctail: CoctailPartialWithoutId) -> CoctailPartial:
        doc = coctail.model_dump(by_alias=True, mode="json")

        for ing in doc["ingridients"]:
            ing["id"] = ObjectId(ing["id"])
        for glass in doc["glasses"]:
            glass["id"] = ObjectId(glass["id"])

        res = await self._collection.insert_one(add_metadata(doc))
        return CoctailPartial(
            id=CoctailId(str(res.inserted_id)),
            name=coctail.name,
            description=coctail.description,
            ingridients=coctail.ingridients,
            glasses=coctail.glasses,
        )

    async def get_by_id(self, id: CoctailId) -> CoctailPartial:
        res = await self._collection.find_one({"_id": ObjectId(id)})
        if res is None:
            raise DocumentNotFound(f"Coctail with {id=} not found")

        return self._parse_doc(res)

    async def get_all(self) -> list[CoctailPartial]:
        cur = self._collection.find()
        return list(map(self._parse_doc, await cur.to_list(length=None)))

    @staticmethod
    def _parse_doc(doc: Mapping[str, Any]) -> CoctailPartial:
        doc = dict(doc)
        doc["id"] = str(doc["_id"])
        doc["ingridients"] = [
            dict(id=str(ingridient["id"]), amount=ingridient["amount"])
            for ingridient in doc["ingridients"]
        ]
        doc["glasses"] = [dict(id=str(glass["id"])) for glass in doc["glasses"]]

        return CoctailPartial.model_validate(doc)
