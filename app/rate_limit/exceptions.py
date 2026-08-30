class RateLimitError(Exception):
    """
    Base exception for rate-limiter errors.
    """

    pass


class RateLimitStorageError(RateLimitError):
    """
    Raised when the rate limiter cannot communicate with
    its backing storage, such as Redis.
    """

    pass