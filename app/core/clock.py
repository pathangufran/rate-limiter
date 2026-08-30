import time

class Clock:
    """
    Provides the current Unix timestamp.

    Keeping time behind an abstraction makes the rate-limiter
    algorithms easier to test because tests can inject a fake clock.
    """

    def now(self) -> int:
        """
        Return the current Unix timestamp in seconds.
        """
        return int(time.time())