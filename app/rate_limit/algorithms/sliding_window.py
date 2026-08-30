from uuid import UUID,uuid4
from redis.asyncio import Redis
from redis.exceptions import RedisError
from app.core.clock import Clock
from app.rate_limit.result import RateLimitResult
from app.rate_limit.algorithms.base import (
    RateLimitAlgorithm,
)
from app.rate_limit.exceptions import (
    RateLimitStorageError,
)
from app.rate_limit.policy import (
    RateLimitPolicyConfig,
)
from app.rate_limit.state import (
    build_sliding_window_key,
)

class SlidingWindowAlgorithm(RateLimitAlgorithm):

    def __init__(self,clock: Clock):
        self.clock = clock

    async def check(
        self,
        *,
        redis: Redis,
        rule_id: UUID,
        identity_key: str,
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

        now = self.clock.now()
        window_start = (
            now - policy.window_seconds
        )
        key = build_sliding_window_key(
            rule_id=rule_id,
            identity_key=identity_key,
        )
        request_id = str(uuid4())

        try:
            await redis.zremrangebyscore(
                key,
                "-inf",
                window_start,
            )
            current_count = await redis.zcard(key)
            if current_count >= (
                policy.request_limit
            ):
                retry_after = (
                    await self.__calculate_retry_after(
                        redis=redis,
                        key=key,
                        now=now,
                        window_seconds=(
                            policy.window_seconds
                        ),
                    )
                )
                return RateLimitResult(
                    allowed=False,
                    limit=policy.request_limit,
                    remaining=0,
                    retry_after=retry_after,
                    reset_after=retry_after,
                    reason="rate_limit_exceeded",
                )

            await redis.zadd(
                key,
                {request_id: now,}
            )
            await redis.expire(
                key,
                policy.window_seconds,
            )
            new_count = current_count + 1
            remaining = max(
                0,
                policy.request_limit - new_count,
            )

            return RateLimitResult(
                allowed=True,
                limit=policy.request_limit,
                remaining=remaining,
                retry_after=None,
                reset_after=(
                    policy.window_seconds
                ),
                reason=None,
            )

        except RedisError as exc:
            raise RateLimitStorageError(
                "Unable to evaluate sliding window rate limit"
            ) from exc

    async def _calculate_retry_after(
        self,
        *,
        redis: Redis,
        key: str,
        now: int,
        window_seconds: int,
    ) -> int:

        oldest = await redis.zrange(
            key,
            0,
            0,
            withscores=True,
        )
        if not oldest:
            return 1
        
        oldest_timestamp = int(oldest[0][1])
        retry_after = (
            oldest_timestamp
            + window_seconds
            - now
        )

        return max(1,retry_after,)