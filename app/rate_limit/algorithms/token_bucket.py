import math
from uuid import UUID   
from decimal import Decimal
from redis.asyncio import Redis
from redis.exceptions import RedisError
from app.core.clock import Clock 
from app.rate_limit.algorithms.base import (
    RateLimitAlgorithm,
)
from app.rate_limit.result import RateLimitResult
from app.rate_limit.policy import RateLimitPolicyConfig
from app.rate_limit.exceptions import RateLimitStorageError
from app.rate_limit.state import build_token_bucket_key

class TokenBucketAlgorithm(RateLimitAlgorithm):

    def __init__(self,clock: Clock):
        self.clock = clock

    async def check(
        self,
        *,
        redis: Redis,
        rule_id: UUID,
        identity_key:str,
        policy: RateLimitPolicyConfig,
    ) -> RateLimitResult:

        if policy.burst_capacity is None:
            raise ValueError(
                "burst_capacity is required"
            )
        if policy.refill_rate is None:
            raise ValueError(
                "refill_rate is required"
            )
        if policy.burst_capacity <= 0:
            raise ValueError(
                "burst_capacity must be greater than zero"
            )
        if policy.refill_rate <= 0:
            raise ValueError(
                "refill_rate must be greater than zero"
            )

        now = self.clock.now()

        key = build_token_bucket_key(
            rule_id=rule_id,
            identity_key=identity_key,
        )

        request_cost = 1

        try:
            state = await redis.hgetall(key)
            if not state:
                current_tokens = Decimal(
                    policy.burst_capacity
                )
                last_refill = now

            else:
                current_tokens = Decimal(state["tokens"])
                last_refill = int(state["last_refill"])

            elapsed = max(0,now-last_refill,)
            refill = (
                Decimal(str(policy.refill_rate))
                * Decimal(elapsed)
            )
            available_tokens = min(
                Decimal(policy.burst_capacity),
                current_tokens + refill,
            )
            if available_tokens < request_cost:
                retry_after = self._calculate_retry_after(
                    available_tokens=(available_tokens),
                    request_cost=request_cost,
                    refill_rate=(
                        Decimal(str(policy.refill_rate))
                    ),
                )

                return RateLimitResult(
                    allowed=False,
                    limit=policy.burst_capacity,
                    remaining=int(available_tokens),
                    retry_after=retry_after,
                    reset_after=retry_after,
                    reason="rate_limit_exceeded",
                )

            remaining_tokens = (
                available_tokens - request_cost
            )
            await redis.hset(
                key,
                mapping={
                    "tokens": str(
                        remaining_tokens
                    ),
                    "last_refill": str(now),
                },
            )
            await redis.expire(
                key,
                self._calculate_ttle(policy=policy),
            )

            return RateLimitResult(
                allowed=True,
                limit=policy.burst_capacity,
                remaining=int(remaining_tokens),
                retry_after=None,
                reset_after=(
                    self._calculate_reset_after(
                        tokens=remaining_tokens,
                        capacity=(
                            Decimal(policy.burst_capacity)
                        ),
                        refill_rate=(
                            Decimal(str(policy.refill_rate))
                        ),
                    )
                ),
                reason=None,
            )

        except RedisError as exc:
            raise RateLimitStorageError(
                "Unable to evaluate token bucket rate limit"
            ) from exc

    @staticmethod
    def _calculate_retry_after(
        *,
        available_tokens: Decimal,
        request_cost: int,
        refill_rate: Decimal,
    ) -> int:

        required = (
            Decimal(request_cost) - available_tokens
        )
        seconds = (
            required / refill_rate
        )

        return max(1,math.ceil(float(seconds)))

    @staticmethod
    def _calculate_reset_after(
        *,
        tokens: Decimal,
        capacity: Decimal,
        refill_rate: Decimal,
    ) -> int:

        missing = (capacity - tokens)
        if missing <= 0:
            return 0

        seconds = (missing / refill_rate)

        return max(0,math.ceil(float(seconds)))

    @staticmethod
    def _calculate_ttl(
        *,
        policy: RateLimitPolicyConfig,
    ) -> int:

        refill_rate = Decimal(str(policy.refill_rate))
        capacity = Decimal(policy.burst_capacity)
        second_to_full = (capacity / refill_rate)

        return max(
            60,
            math.ceil(float(second_to_full)) + 60,
        )
