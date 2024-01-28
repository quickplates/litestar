from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)


class BadRequestException(HTTPException):
    """Bad Request."""

    status_code = HTTP_400_BAD_REQUEST
    detail = "Bad Request"


class UnauthorizedException(HTTPException):
    """Unauthorized."""

    status_code = HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"


class ForbiddenException(HTTPException):
    """Forbidden."""

    status_code = HTTP_403_FORBIDDEN
    detail = "Forbidden"


class NotFoundException(HTTPException):
    """Not Found."""

    status_code = HTTP_404_NOT_FOUND
    detail = "Not Found"


class ConflictException(HTTPException):
    """Conflict."""

    status_code = HTTP_409_CONFLICT
    detail = "Conflict"


class UnprocessableContentException(HTTPException):
    """Unprocessable Content."""

    status_code = HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Unprocessable Content"


class InternalServerErrorException(HTTPException):
    """Internal Server Error."""

    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"


class ServiceUnavailableException(HTTPException):
    """Service Unavailable."""

    status_code = HTTP_503_SERVICE_UNAVAILABLE
    detail = "Service Unavailable"
