import asyncio
from collections.abc import Iterable
from typing import Annotated

from pydantic.types import PositiveInt, confrozenset

from .client import get_client
from .coctails_storage import (
    CoctailId,
    CoctailIngridientPartial,
    CoctailPartial,
    CoctailPartialWithoutId,
    CoctailsStorage,
)
from .commons import ApiBaseModel, Description, DocumentNotFound, Name
from .glasses_storage import Glass, GlassesStorage, GlassId, GlassWithoutId
from .ingridients_storage import (
    Ingridient,
    IngridientId,
    IngridientsStorage,
    IngridientWithoutId,
)

DB_NAME = "coctails"


class CoctailIngridient(Ingridient):
    amount: PositiveInt


class Coctail(ApiBaseModel):
    id: CoctailId
    name: Name
    description: Description
    ingridients: Annotated[
        frozenset[CoctailIngridient], confrozenset(CoctailIngridient, min_length=1)
    ]
    glasses: Annotated[frozenset[Glass], confrozenset(Glass, min_length=1)]


class Storage:
    def __init__(
        self,
        ingridients_storage: IngridientsStorage,
        glasses_storage: GlassesStorage,
        coctails_storage: CoctailsStorage,
    ) -> None:
        self._ingridients_storage = ingridients_storage
        self._glasses_storage = glasses_storage
        self._coctails_storage = coctails_storage

    async def save_ingridient(self, ingridient: IngridientWithoutId) -> Ingridient:
        return await self._ingridients_storage.save(ingridient)

    async def get_ingridient_by_id(self, ingridient_id: IngridientId) -> Ingridient:
        return await self._ingridients_storage.get_by_id(ingridient_id)

    async def get_ingridients(self) -> list[Ingridient]:
        return await self._ingridients_storage.get_all()

    async def save_glass(self, glass: GlassWithoutId) -> Glass:
        return await self._glasses_storage.save(glass)

    async def get_glass_by_id(self, glass_id: GlassId) -> Glass:
        return await self._glasses_storage.get_by_id(glass_id)

    async def get_glasses(self) -> list[Glass]:
        return await self._glasses_storage.get_all()

    async def save_coctail(self, coctail: CoctailPartialWithoutId) -> Coctail:
        try:
            async with asyncio.TaskGroup() as tg:
                ingridient_tasks = [
                    tg.create_task(self.get_ingridient_by_id(ingridient.id))
                    for ingridient in coctail.ingridients
                ]
                glass_tasks = [
                    tg.create_task(self.get_glass_by_id(glass.id))
                    for glass in coctail.glasses
                ]
        except ExceptionGroup:
            raise DocumentNotFound("Some of the parts not found")

        res = await self._coctails_storage.save(coctail)
        return Coctail(
            id=res.id,
            name=coctail.name,
            description=coctail.description,
            ingridients=self._get_ingridients_from_tasks(
                zip(coctail.ingridients, ingridient_tasks, strict=True)
            ),
            glasses=frozenset(glass_task.result() for glass_task in glass_tasks),
        )

    async def get_coctail_by_id(self, coctail_id: CoctailId) -> Coctail:
        coctail_partial = await self._coctails_storage.get_by_id(coctail_id)

        return await self._populate_partial_coctail(coctail_partial)

    async def get_coctails(self) -> list[Coctail]:
        coctails_partial = await self._coctails_storage.get_all()
        return [
            await self._populate_partial_coctail(coctail_partial)
            for coctail_partial in coctails_partial
        ]

    @staticmethod
    def _get_ingridients_from_tasks(
        ingridients: Iterable[
            tuple[CoctailIngridientPartial, asyncio.Task[Ingridient]]
        ],
    ) -> frozenset[CoctailIngridient]:
        return frozenset(
            CoctailIngridient(
                id=ingridient_task.result().id,
                name=ingridient_task.result().name,
                description=ingridient_task.result().description,
                amount=ingridient.amount,
            )
            for ingridient, ingridient_task in ingridients
        )

    async def _populate_partial_coctail(
        self, coctail_partial: CoctailPartial
    ) -> Coctail:
        # TODO: consifer using MongoDB aggregation pipeline
        try:
            async with asyncio.TaskGroup() as tg:
                ingridient_tasks = [
                    tg.create_task(self.get_ingridient_by_id(ingridient.id))
                    for ingridient in coctail_partial.ingridients
                ]
                glass_tasks = [
                    tg.create_task(self.get_glass_by_id(glass.id))
                    for glass in coctail_partial.glasses
                ]
        except ExceptionGroup:
            raise DocumentNotFound("Some of the parts not found")

        return Coctail(
            id=coctail_partial.id,
            name=coctail_partial.name,
            description=coctail_partial.description,
            ingridients=self._get_ingridients_from_tasks(
                zip(coctail_partial.ingridients, ingridient_tasks, strict=True)
            ),
            glasses=frozenset(glass_task.result() for glass_task in glass_tasks),
        )


def get_storage() -> Storage:
    mongo_client = get_client()
    db = mongo_client[DB_NAME]
    ingridients_storage = IngridientsStorage(db)
    glasses_storage = GlassesStorage(db)
    coctails_storage = CoctailsStorage(db)
    return Storage(ingridients_storage, glasses_storage, coctails_storage)
