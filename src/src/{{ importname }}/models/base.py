from dataclasses import Field, dataclass, field
from typing import dataclass_transform

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


@dataclass_transform(
    # Generate __eq__ method
    eq_default=True,
    # Don't generate __lt__, __le__, __gt__, __ge__ methods
    order_default=False,
    # Make all fields keyword-only
    kw_only_default=True,
    # Make the instance immutable
    frozen_default=True,
    # Allow using dataclass field specifiers
    field_specifiers=(Field, field),
)
def datamodel[T](cls: type[T] | None = None, /, *, order: bool = False) -> type[T]:
    """Transform a class into a data model."""

    return dataclass(
        cls,
        eq=True,
        order=order,
        kw_only=True,
        frozen=True,
    )


class SerializableModel(BaseModel):
    """Base class for models that can be serialized to JSON."""

    model_config = ConfigDict(
        # Ignore extra fields
        extra="ignore",
        # Make the instance immutable
        frozen=True,
        # Allow populating aliased fields by their original name
        populate_by_name=True,
        # Disallow arbitrary types that Pydantic can't handle
        arbitrary_types_allowed=False,
        # Add camelCase aliases for all fields
        alias_generator=to_camel,
        # Disallow non-serializable float values
        allow_inf_nan=False,
        # Allow type coercion
        strict=False,
        # Validate default values
        validate_default=True,
        # Make fields with default values required in serialization schemas
        json_schema_serialization_defaults_required=True,
        # Allow coercion of numbers to strings
        coerce_numbers_to_str=True,
        # Use field docstrings as descriptions
        use_attribute_docstrings=True,
    )
