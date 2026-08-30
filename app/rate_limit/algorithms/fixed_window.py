from redis.asyncio import Redis
from app.rate_limit.algorithms.base import (
    RateLimitAlgorithm,
)
from app.rate_limit.policy import (
    RateLimitPolicyConfig,
)
from app.rate_limit.result import RateLimitResult

class FixedWindowAlgorithm(RateLimitAlgorithm):

    async def check(
        self,
        *,
        redis: Redis,
        key: str,
        policy: RateLimitPolicyConfig,
    ) -> RateLimitResult:

        return NotImplementedError(
            "Fixed Window will be implemented in Module 2"   
        )