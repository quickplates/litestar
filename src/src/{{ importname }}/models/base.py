from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SerializableModel(BaseModel):
    """Base class for models that can be serialized to JSON."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
