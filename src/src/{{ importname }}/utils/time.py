from datetime import UTC, datetime, timedelta
from email.utils import format_datetime, parsedate_to_datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import AfterValidator, Field
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


def awareutcnow() -> UTCDatetime:
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
