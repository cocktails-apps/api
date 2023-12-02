from typing import Optional

from .base import BaseModel


class Ingridient(BaseModel):
    name: str
    description: str


class Glass(BaseModel):
    name: str
    description: str


class Coctail(BaseModel):
    name: str
    description: Optional[str]
    ingredients: list[Ingridient]
    glass_type: list[Glass]
