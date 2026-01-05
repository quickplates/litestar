from datetime import UTC, datetime
from email.utils import format_datetime, parsedate_to_datetime
from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AfterValidator, Field, TypeAdapter
from pydantic import NaiveDatetime as PydanticNaiveDatetime


def awareutcnow() -> datetime:
    """Return the current datetime in UTC with timezone information."""
    return datetime.now(UTC)


def naiveutcnow() -> datetime:
    """Return the current datetime in UTC without timezone information."""
    return awareutcnow().replace(tzinfo=None)


def stringify(dt: datetime) -> str:
    """Convert a datetime to a string in ISO 8601 format."""
    return dt.isoformat().replace("+00:00", "Z")


def httpparse(value: str) -> datetime:
    """Parse an HTTP date string to a datetime."""
    return parsedate_to_datetime(value)


def httpstringify(dt: datetime) -> str:
    """Convert a datetime to an HTTP date string."""
    return format_datetime(dt, usegmt=True)


class TimezoneValidationError(ValueError):
    """Timezone validation error."""

    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid time zone: {value}")


def validate_timezone(value: str) -> str:
    """Validate a time zone."""
    try:
        ZoneInfo(value)
    except ZoneInfoNotFoundError as e:
        raise TimezoneValidationError(value) from e

    return value


Timezone = Annotated[
    str,
    AfterValidator(validate_timezone),
    Field(examples=["Europe/Warsaw"]),
]


def validate_naive_datetime(value: datetime) -> datetime:
    """Validate a naive datetime."""
    return TypeAdapter(PydanticNaiveDatetime).validate_python(value)


NaiveDatetime = Annotated[
    datetime,
    AfterValidator(validate_naive_datetime),
    Field(examples=["2025-01-01T00:00:00"]),
]
