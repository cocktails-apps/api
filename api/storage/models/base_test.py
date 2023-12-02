from .base import BaseModel


def test_base_model_json():
    class Model(BaseModel):
        some_value: str

    m = Model(some_value="test")

    doc = m.model_dump(by_alias=True)
    assert doc == {"someValue": "test"}
