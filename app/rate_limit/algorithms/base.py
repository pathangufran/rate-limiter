from abc import ABC, abstractmethod
from redis.asyncio import Redis
from app.rate_limit.policy import RateLimitPolicyConfig
from app.rate_limit.result import RateLimitResult

class RateLimitAlgorithm(ABC):
    """
    Base contract implemented by every rate-limit algorithm.
    """

    @abstractmethod
    async def check(
        self,
        *,
        redis: Redis,
        key: str,
        policy: RateLimitPolicyConfig,
    ) -> RateLimitResult:
        """
        Atomically evaluate a request against the policy.
        """
        
        raise NotImplementedError