from enum import Enum
from dataclasses import dataclass

class RateLimitFailureMode(str,Enum):
    """
    Determines what happens when the rate-limit
    system cannot evaluate a request.
    """

    FAIL_OPEN = "file_open"
    FAIL_CLOSED = "file_closed"

@dataclass(frozen=True)
class RateLimitFailurePolicy:
    """
    Defines how the system behaves when
    rate-limit evaluation fails.
    """

    mode: RateLimitFailureMode = (
        RateLimitFailureMode.FAIL_OPEN
    ) 

    def should_allow(self) -> bool:
        """
        Determine whether the request should
        be allowed when rate limiting fails.
        """

        return (
            self.mode 
            == RateLimitFailureMode.FAIL_OPEN
        )