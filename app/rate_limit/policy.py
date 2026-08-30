from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from app.core.enums import RateLimitAlgorithm

@dataclass(frozen=True)
class RateLimitPolicyConfig:

    id: UUID
    algorithm: RateLimitAlgorithm
    request_limit: int | None
    window_seconds: int | None
    burst_capacity: int | None
    refill_rate: Decimal | None

    