from collections import defaultdict
from pydantic import ValidationError


class AppException(Exception):
    """Root of exception tree"""

    def __init__(self, status_code=500, /, *args):
        super().__init__(*args)

        self.status_code = status_code


class DomainException(AppException):
    """Business login"""

    def __init__(self, *args):
        super().__init__(404, *args)


class RepositoryException(AppException):
    """Data storage"""

    def __init__(self, *args):
        super().__init__(500, *args)


class ExternalServiceException(AppException):
    """External services (exterlan api calls)"""

    def __init__(self, *args):
        super().__init__(404, *args)


class NotFoundException(RepositoryException):
    """No such entry in DB"""


class TvMazeException(ExternalServiceException):
    """Something wrong with TV maze"""


class TvMazeRateLimitException(ExternalServiceException):
    """Slow down, to many requests"""


def pydantic_error_to_dict(e: ValidationError) -> dict:
    result = defaultdict(list)

    for err in e.errors():
        result[".".join(map(str, err["loc"]))].append(err["msg"])
    return result
