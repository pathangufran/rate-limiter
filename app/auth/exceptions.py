class AuthenticationError(Exception):
    """
    Base authentication exception.
    """

    pass


class InvalidAPIKeyError(
    AuthenticationError
):
    """
    Raised when an API key is invalid,
    inactive, or expired.
    """

    pass