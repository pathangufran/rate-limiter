from dataclasses import dataclass

@dataclass(frozen=True)
class RateLimitResult:

    allowed: bool
    limit: int | None
    remaining: int | None
    retry_after: int | None
    reset_after: int | None
    reason: str | None = None

    def __post_init__(self):

        if self.limit < 0:
            raise ValueError(
                "limit cannot be negative"
            )
        if self.remaining < 0:
            raise ValueError(
                "remaining cannot be negative"
            )
        if self.reset_after < 0:
            raise ValueError(
                "reset_after cannot be negative"
            )

        if (
            self.retry_after is not None
            and self.retry_after < 0
        ):
            raise ValueError(
                "retry_after cannot be negative"
            )