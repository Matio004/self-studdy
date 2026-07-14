class AppException(Exception):
    """Root of exception tree"""


class DomainException(AppException):
    """Business login"""


class RepositoryException(AppException):
    """Data storage"""


class ExternalServiceException(AppException):
    """External services (exterlan api calls)"""


class NotFoundException(RepositoryException):
    """No such entry in DB"""


class TvMazeException(ExternalServiceException):
    """Something wrong with TV maze"""


class TvMazeRateLimitException(ExternalServiceException):
    """Slow down, to many requests"""
