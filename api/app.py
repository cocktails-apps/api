from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from .routes import (
    register_coctails_routes,
    register_glasses_routes,
    register_info_routes,
    register_ingridients_routes,
)
from .storage import get_storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    storage = get_storage()
    register_info_routes(app)
    register_coctails_routes(app, storage)
    register_glasses_routes(app, storage)
    register_ingridients_routes(app, storage)

    yield


app = FastAPI(lifespan=lifespan)
