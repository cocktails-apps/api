from fastapi import APIRouter, FastAPI
from pydantic import BaseModel


class Coctail(BaseModel):
    name: str
    description: str


Coctails = list[Coctail]


def register_coctails_routes(app: FastAPI) -> None:
    router = APIRouter(prefix="/coctails")

    @router.get("/")
    def get() -> Coctails:
        return [Coctail(name="screwdriver", description="Cool coctail.")]

    app.include_router(router)
