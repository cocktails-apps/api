from typing import ClassVar, Optional

from bson import ObjectId
from pydantic import ConfigDict
from typing_extensions import LiteralString

from .base import BASE_CONFIG, BaseModel


class BaseDocument(BaseModel):
    model_config = ConfigDict(**BASE_CONFIG, arbitrary_types_allowed=True)
    collection_name: ClassVar[LiteralString]

    id: ObjectId


class IngridientDocument(BaseDocument):
    collection_name = "ingridients"

    name: str
    description: str


class GlassDocument(BaseDocument):
    collection_name = "glasses"

    name: str
    description: str


class CoctailDocument(BaseDocument):
    collection_name = "coctails"

    name: str
    description: Optional[str]
    ingredients: list[ObjectId]
    glass_type: list[ObjectId]
