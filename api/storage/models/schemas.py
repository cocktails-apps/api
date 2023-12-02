from typing import NewType

from .base import BaseModel

IngridientId = NewType("IngridientId", str)


class Ingridient(BaseModel):
    id: IngridientId
    name: str
    description: str


class IngridientUpload(BaseModel):
    name: str
    description: str


GlassId = NewType("GlassId", str)


class Glass(BaseModel):
    id: GlassId
    name: str
    description: str


class GlassUpload(BaseModel):
    name: str
    description: str


CoctailId = NewType("CoctailId", str)


class Coctail(BaseModel):
    id: CoctailId
    name: str
    description: str
    ingredients: list[Ingridient]
    glass_type: list[Glass]


class CoctailIngridientUpload(BaseModel):
    id: IngridientId


class CoctailGlassUpload(BaseModel):
    id: GlassId


class CoctailUpload(BaseModel):
    name: str
    description: str
    ingredients: list[CoctailIngridientUpload]
    glass_type: list[CoctailGlassUpload]
