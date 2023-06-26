from datetime import datetime


def stringify(dt: datetime) -> str:
    """Convert a datetime to a string in ISO 8601 format"""

    return dt.isoformat().replace("+00:00", "Z")
