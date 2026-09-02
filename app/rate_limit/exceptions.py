class RateLimitError(Exception):
    """
    Base exception for all rate-limit failures.
    """


class RateLimitBackendError(
    RateLimitError
):
    """
    Raised when the rate-limit backend
    cannot be reached or used.
    """


class RateLimitBackendTimeout(
    RateLimitBackendError
):
    """
    Raised when the rate-limit backend
    takes too long to respond.
    """


class RateLimitBackendUnavailable(
    RateLimitBackendError
):
    """
    Raised when the rate-limit backend
    is unavailable.
    """


class RateLimitEvaluationError(
    RateLimitError
):
    """
    Raised when rate-limit evaluation
    cannot be completed.
    """