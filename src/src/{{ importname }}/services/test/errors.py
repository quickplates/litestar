class ServiceError(Exception):
    """Base class for service errors."""


class ValidationError(ServiceError):
    """Raised when a validation error occurs."""


class MessageTooLongError(ValidationError):
    """Raised when message is too long."""

    def __init__(self, message: str, limit: int) -> None:
        super().__init__(
            f"Message has {len(message)} characters, which exceeds the limit of {limit}."
        )
