from fastapi import FastAPI

from .routes import register_coctails_routes, register_info_routes

app = FastAPI()

register_info_routes(app)
register_coctails_routes(app)
