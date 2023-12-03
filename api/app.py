from fastapi import FastAPI

from .routes import register_coctails_routes, register_info_routes
from .storage import get_storage

app = FastAPI()
storage = get_storage()

register_info_routes(app)
register_coctails_routes(app, storage)
