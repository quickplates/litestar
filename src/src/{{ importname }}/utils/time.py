from datetime import UTC, datetime, timedelta
from email.utils import format_datetime, parsedate_to_datetime
from functools import partial
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import (
    AfterValidator,
    BeforeValidator,
    Field,
    PlainSerializer,
    TypeAdapter,
)
from pydantic import AwareDatetime as PydanticAwareDatetime
from pydantic import NaiveDatetime as PydanticNaiveDatetime
from pydantic.json_schema import Examples, WithJsonSchema

type AwareDatetime = Annotated[
    PydanticAwareDatetime,
    Field(description="Datetime with timezone."),
    Examples(["2000-01-01T00:00:00Z"]),
]

type NaiveDatetime = Annotated[
    PydanticNaiveDatetime,
    Field(description="Datetime without timezone."),
    Examples(["2000-01-01T00:00:00"]),
]


def validate_utc_datetime(value: AwareDatetime) -> AwareDatetime:
    """Validate that the datetime is in UTC."""
    if value.tzinfo != UTC:
        msg = f"Datetime must be in UTC, got {value.tzinfo}"
        raise ValueError(msg)

    return value


type UTCDatetime = Annotated[
    PydanticAwareDatetime,
    Field(description="Datetime in UTC."),
    AfterValidator(validate_utc_datetime),
    Examples(["2000-01-01T00:00:00Z"]),
]


type HTTPDatetime = Annotated[
    UTCDatetime,
    BeforeValidator(
        lambda value: parsedate_to_datetime(value) if isinstance(value, str) else value,
        json_schema_input_type=str,
    ),
    PlainSerializer(partial(format_datetime, usegmt=True), return_type=str),
    WithJsonSchema({"type": "string", "description": "Datetime in HTTP format."}),
    Examples(["Sat, 01 Jan 2000 00:00:00 GMT"]),
]


type Timezone = Annotated[
    ZoneInfo,
    WithJsonSchema({"type": "string", "description": "Timezone name."}),
    Examples(["Europe/Warsaw"]),
]


type Timedelta = Annotated[
    timedelta,
    Field(description="Duration of time."),
    Examples(["PT1H"]),
]


def awareutcnow() -> datetime:
    """Return the current datetime in UTC with timezone information."""
    return datetime.now(UTC)


def naiveutcnow() -> datetime:
    """Return the current datetime in UTC without timezone information."""
    return awareutcnow().replace(tzinfo=None)


def isostringify(dt: datetime) -> str:
    """Convert a datetime to a string in ISO 8601 format."""
    return TypeAdapter(datetime).dump_python(dt, mode="json")


def isoparse(value: str) -> datetime:
    """Parse a string in ISO 8601 format to a datetime."""
    return TypeAdapter(datetime).validate_python(value)


def httpstringify(dt: datetime) -> str:
    """Convert a datetime to an HTTP date string."""
    return TypeAdapter(HTTPDatetime).dump_python(dt, mode="json")


def httpparse(value: str) -> datetime:
    """Parse an HTTP date string to a datetime."""
    return TypeAdapter(HTTPDatetime).validate_python(value)
