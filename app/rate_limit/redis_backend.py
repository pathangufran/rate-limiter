from app.rate_limit.exceptions import (
    RateLimitBackendError,
    RateLimitBackendTimeout,
    RateLimitBackendUnavailable,
)

class RateLimitRedisBackend:

    def __init__(self,redis):
        self.redis = redis

    async def get(
        self,
        key: str,
    ):
        try:
            return await self.redis.get(key)

        except TimeoutError as exc:
            raise RateLimitBackendTimeout(
                "Redis opeartion timed out"
            ) from exc

        except ConnectionError as exc:
            raise RateLimitBackendUnavailable(
                "Redis connection failed"
            ) from exc

        except Exception as exc:
            raise RateLimitBackendError(
                "Redis operation failed"
            ) from exc

    async def set(
        self,
        key: str,
        value,
        *,
        ex: int | None = None,
    ):
        try:
            return await self.redis.set(
                key,
                value,
                ex=ex,
            )

        except TimeoutError as exc:
            raise RateLimitBackendTimeout(
                "Redis opeartions time out"
            ) from exc

        except ConnectionError as exc:
            raise RateLimitBackendUnavailable(
                "Redis connection failed"
            ) from exc

        except Exception as exc:
            raise RateLimitBackendError(
                "Redis operations failed"
            ) from exc

    async def incr(
        self,
        key: str,
    ):
        try:
            return await self.redis.incr(key)

        except TimeoutError as exc:
            raise RateLimitBackendTimeout(
                "Redis operations timed out"
            ) from exc

        except ConnectionError as exc:
            raise RateLimitBackendUnavailable(
                "Redis connection failed"
            ) from exc

        except Exception as exc:
            raise RateLimitBackendError(
                "Redis operations failed"
            ) from exc

    async def expire(
        self,
        key: str,
        seconds: int,
    ): 
        try:
            return await self.redis.expire(
                key,
                seconds,
            )

        except TimeoutError as exc:
            raise RateLimitBackendTimeout(
                "Redis operations timed out"
            ) from exc

        except ConnectionError as exc:
            raise RateLimitBackendUnavailable(
                "Redis connection failed"
            ) from exc

        except Exception as exc:
            raise RateLimitBackendError(
                "Redis operation failed"
            ) from exc