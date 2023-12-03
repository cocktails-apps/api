from fastapi import FastAPI

from .routes import register_coctails_routes, register_info_routes
from .storage import get_client

mongo_client = get_client()


app = FastAPI()


register_info_routes(app, mongo_client)
register_coctails_routes(app)
