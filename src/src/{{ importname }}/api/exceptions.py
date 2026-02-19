from litestar import exceptions as le
from litestar import status_codes as c

BadRequestException = le.ValidationException

UnauthorizedException = le.NotAuthorizedException

ForbiddenException = le.PermissionDeniedException

NotFoundException = le.NotFoundException


class ConflictException(le.ClientException):
    """Conflict."""

    status_code = c.HTTP_409_CONFLICT
    detail = "Conflict"


InternalServerErrorException = le.InternalServerException

ServiceUnavailableException = le.ServiceUnavailableException
