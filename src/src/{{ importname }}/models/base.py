from collections.abc import Callable
from dataclasses import Field, dataclass, field
from typing import Any, dataclass_transform, get_args, overload, override

from pydantic import BaseModel, ConfigDict, Json, RootModel
from pydantic.alias_generators import to_camel

CONFIG = ConfigDict(
    # Add camelCase aliases for all fields
    alias_generator=to_camel,
    # Disallow non-serializable float values
    allow_inf_nan=False,
    # Allow coercion of numbers to strings
    coerce_numbers_to_str=True,
    # Make the instance immutable
    frozen=True,
    # Make fields with default values required in serialization schemas
    json_schema_serialization_defaults_required=True,
    # Serialize aliased fields by their alias
    serialize_by_alias=True,
    # Preserve empty paths in URLs
    url_preserve_empty_path=True,
    # Use field docstrings as descriptions
    use_attribute_docstrings=True,
    # Allow populating aliased fields by their original name
    validate_by_name=True,
    # Validate default values
    validate_default=True,
    # Validate return values from callable validators
    validate_return=True,
    # Attach underlying exceptions as cause for validation errors
    validation_error_cause=True,
)


class SerializableModel(BaseModel):
    """Base class for serializable models."""

    model_config = CONFIG


class Serializable[T](RootModel[T]):
    """Base class for serializable root models."""

    model_config = CONFIG

    @classmethod
    def __get_annotation__(cls) -> Any:
        return cls.model_fields["root"].annotation

    @classmethod
    def __get_title__(cls) -> str:
        return getattr(cls.__get_annotation__(), "__name__", cls.__name__)

    @override
    @classmethod
    def __pydantic_on_complete__(cls) -> None:
        cls.__annotation__ = cls.__get_annotation__()
        cls.model_config["model_title_generator"] = lambda cls: cls.__get_title__()


class Jsonable[T](Serializable[T | Json[T]]):
    """Base class for JSON-serializable root models."""

    @override
    @classmethod
    def __get_annotation__(cls) -> Any:
        return get_args(cls.model_fields["root"].annotation)[0]


@overload
def datamodel[T](cls: type[T], /, *, order: bool = False) -> type[T]: ...
@overload
def datamodel[T](
    cls: None = None, /, *, order: bool = False
) -> Callable[[type[T]], type[T]]: ...
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
def datamodel[T](
    cls: type[T] | None = None, /, *, order: bool = False
) -> type[T] | Callable[[type[T]], type[T]]:
    """Transform a class into a data model."""
    return dataclass(
        cls,
        eq=True,
        order=order,
        kw_only=True,
        frozen=True,
    )
