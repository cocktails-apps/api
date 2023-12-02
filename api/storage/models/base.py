import humps
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

BASE_CONFIG = ConfigDict(
    alias_generator=humps.camelize,
    populate_by_name=True,
    frozen=True,
)


class BaseModel(PydanticBaseModel):
    model_config = BASE_CONFIG
