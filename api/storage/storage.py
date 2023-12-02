import asyncio
from typing import LiteralString

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from .models import (
    Coctail,
    CoctailDocument,
    CoctailId,
    CoctailUpload,
    Glass,
    GlassDocument,
    GlassId,
    GlassUpload,
    Ingridient,
    IngridientDocument,
    IngridientId,
    IngridientUpload,
)

DB_NAME = "coctails"


class DocumentNotFound(ValueError):
    def __init__(self, collection: LiteralString, reason: str) -> None:
        self.collection = collection
        super().__init__(f"Document not found in {collection}: {reason}")


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

    async def save_ingridient(self, ingridient: IngridientUpload) -> Ingridient:
        res = await self._ingridients.insert_one(ingridient.model_dump(by_alias=True))
        return Ingridient(
            id=str(res.inserted_id),
            name=ingridient.name,
            description=ingridient.description,
        )

    async def get_ingridient_by_id(self, ingridient_id: IngridientId) -> Ingridient:
        res = await self._ingridients.find_one({"_id": ObjectId(ingridient_id)})
        if res is None:
            raise DocumentNotFound(
                IngridientDocument.collection_name, f"id={ingridient_id}"
            )

        res["id"] = str(res["_id"])
        return Ingridient.model_validate(res)

    async def save_glass(self, glass: GlassUpload) -> Glass:
        res = await self._glasses.insert_one(glass.model_dump(by_alias=True))
        return Glass(
            id=str(res.inserted_id), name=glass.name, description=glass.description
        )

    async def get_glass_by_id(self, glass_id: GlassId) -> Glass:
        res = await self._glasses.find_one({"_id": ObjectId(glass_id)})
        if res is None:
            raise DocumentNotFound(GlassDocument.collection_name, f"id={glass_id}")

        res["id"] = str(res["_id"])
        return Glass.model_validate(res)

    async def save_coctail(self, coctail: CoctailUpload) -> Coctail:
        try:
            async with asyncio.TaskGroup() as tg:
                ingridient_tasks = [
                    tg.create_task(self.get_ingridient_by_id(ing.id))
                    for ing in coctail.ingredients
                ]
                glass_types_tasks = [
                    tg.create_task(self.get_glass_by_id(glass.id))
                    for glass in coctail.glass_type
                ]
        except ExceptionGroup:
            raise DocumentNotFound(
                CoctailDocument.collection_name, "Some of the parts not found"
            )

        res = await self._coctails.insert_one(
            dict(
                name=coctail.name,
                description=coctail.description,
                ingredients=[ObjectId(ing.id) for ing in coctail.ingredients],
                glassType=[ObjectId(glass.id) for glass in coctail.glass_type],
            )
        )
        return Coctail(
            id=str(res.inserted_id),
            name=coctail.name,
            description=coctail.description,
            ingredients=[ing_task.result() for ing_task in ingridient_tasks],
            glass_type=[glass_task.result() for glass_task in glass_types_tasks],
        )

    async def get_coctail_by_id(self, coctail_id: CoctailId) -> Coctail:
        res = await self._coctails.find_one({"_id": ObjectId(coctail_id)})
        if res is None:
            raise DocumentNotFound(CoctailDocument.collection_name, f"id={coctail_id}")

        # TODO: consifer using MongoDB aggregation pipeline
        async with asyncio.TaskGroup() as tg:
            ingridient_tasks = [
                tg.create_task(self.get_ingridient_by_id(ing_id))
                for ing_id in res["ingredients"]
            ]
            glass_types_tasks = [
                tg.create_task(self.get_glass_by_id(glass_id))
                for glass_id in res["glassType"]
            ]

        res["id"] = str(res["_id"])
        res["ingredients"] = [ing_task.result() for ing_task in ingridient_tasks]
        res["glassType"] = [glass_task.result() for glass_task in glass_types_tasks]
        return Coctail.model_validate(res)

    async def get_coctails(self) -> list[Coctail]:
        return []
