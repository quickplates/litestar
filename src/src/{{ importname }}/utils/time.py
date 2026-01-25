from datetime import UTC, datetime
from email.utils import format_datetime, parsedate_to_datetime
from typing import Annotated
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AfterValidator, Field
from pydantic import (
    AwareDatetime as PydanticAwareDatetime,
)
from pydantic import (
    NaiveDatetime as PydanticNaiveDatetime,
)

AwareDatetime = Annotated[
    PydanticAwareDatetime, Field(examples=["2000-01-01T00:00:00Z"])
]


NaiveDatetime = Annotated[
    PydanticNaiveDatetime, Field(examples=["2000-01-01T00:00:00"])
]


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
    str, AfterValidator(validate_timezone), Field(examples=["Europe/Warsaw"])
]


def awareutcnow() -> AwareDatetime:
    """Return the current datetime in UTC with timezone information."""
    return datetime.now(UTC)


def naiveutcnow() -> NaiveDatetime:
    """Return the current datetime in UTC without timezone information."""
    return awareutcnow().replace(tzinfo=None)


def isostringify(dt: datetime) -> str:
    """Convert a datetime to a string in ISO 8601 format."""
    return dt.isoformat().replace("+00:00", "Z")


def isoparse(value: str) -> datetime:
    """Parse a string in ISO 8601 format to a datetime."""
    return datetime.fromisoformat(value)


def httpstringify(dt: datetime) -> str:
    """Convert a datetime to an HTTP date string."""
    return format_datetime(dt, usegmt=True)


def httpparse(value: str) -> datetime:
    """Parse an HTTP date string to a datetime."""
    return parsedate_to_datetime(value)
