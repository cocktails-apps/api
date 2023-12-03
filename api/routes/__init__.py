from .coctails import register_coctails_routes
from .glasses import register_glasses_routes
from .info import register_info_routes
from .ingridients import register_ingridients_routes

__all__ = [
    "register_coctails_routes",
    "register_glasses_routes",
    "register_info_routes",
    "register_ingridients_routes",
]
