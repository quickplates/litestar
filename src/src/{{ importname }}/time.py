from datetime import datetime, timezone

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
