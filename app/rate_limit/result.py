from dataclasses import dataclass

@dataclass(frozen=True)
class RateLimitResult:

    allowed: bool
    limit: int | None
    remaining: int | None
    retry_after: int | None
    reset_after: int | None
    reason: str | None = None

    