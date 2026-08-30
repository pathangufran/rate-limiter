from redis.asyncio import Redis
from app.rate_limit.algorithms.base import (
    RateLimitAlgorithm,
)
from app.rate_limit.policy import (
    RateLimitPolicyConfig,
)
from app.rate_limit.result import RateLimitResult
from app.rate_limit.time import (
    current_timestamp,
    get_seconds_until_window_reset,
)

class FixedWindowAlgorithm(RateLimitAlgorithm):

    async def check(
        self,
        *,
        redis: Redis,
        key: str,
        policy: RateLimitPolicyConfig,
    ) -> RateLimitResult:

        if policy.request_limit is None:
            raise ValueError(
                "request_limit is required"
            )
        if policy.window_seconds is None:
            raise ValueError(
                "window_seconds is required"
            )

        timestamp = current_timestamp()

        reset_after = (
            get_seconds_until_window_reset(
                timestamp,
                policy.window_seconds,
            )
        )

        current_count = await redis.get(key)
        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count)

        if current_count >= policy.request_limit:

            return RateLimitResult(
                allowed=False,
                limit=policy.request_limit,
                remaining=0,
                retry_after=reset_after,
                reset_after=reset_after,
                reason="rate_limit_exceeded",
            )

        new_count = await redis.incr(key)
        
        if new_count == 1:
            await redis.expire(
                key,
                policy.window_seconds,
            )

        remaining = max(
            0,
            policy.request_limit - new_count
        )

        return RateLimitResult(
            allowed=True,
            limit=policy.request_limit,
            remaining=remaining,
            retry_after=None,
            reset_after=reset_after,
            reason=None,
        )