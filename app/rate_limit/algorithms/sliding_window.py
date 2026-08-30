from redis.asyncio import Redis
from app.rate_limit.algorithms.base import (
    RateLimitAlgorithm,
)
from app.rate_limit.result import RateLimitResult
from app.rate_limit.policy import RateLimitPolicyConfig

class SlidingWindowAlgorithm(RateLimitAlgorithm):

    async def check(
        self,
        *,
        redis: Redis,
        key: str,
        policy: RateLimitPolicyConfig,
    ) -> RateLimitResult:

        raise NotImplementedError(
            "Sliding Window will be implemented in Module 4"
        )