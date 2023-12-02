from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routes import register_coctails_routes, register_info_routes
from .storage import get_client, init_collections

mongo_client = get_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_collections(mongo_client)

    yield


app = FastAPI()


register_info_routes(app, mongo_client)
register_coctails_routes(app)
