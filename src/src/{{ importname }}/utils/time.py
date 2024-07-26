from datetime import datetime, timezone
from email.utils import format_datetime, parsedate_to_datetime

from pydantic import AwareDatetime, NaiveDatetime


def awareutcnow() -> AwareDatetime:
    """Return the current datetime in UTC with timezone information."""

    return datetime.now(timezone.utc)


def naiveutcnow() -> NaiveDatetime:
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
