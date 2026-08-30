from app.core.clock import Clock
from app.core.enums import RateLimitAlgorithm
from app.rate_limit.algorithms.base import (
    RateLimitAlgorithm as Algorithm
)
from app.rate_limit.algorithms.fixed_window import (
    FixedWindowAlgorithm
)
from app.rate_limit.algorithms.sliding_window import (
    SlidingWindowAlgorithm
)
from app.rate_limit.algorithms.token_bucket import (
    TokenBucketAlgorithm
)

class AlgorithmFactory:

    @classmethod
    def create(
        cls,
        algorithm: RateLimitAlgorithm,
        clock: Clock,
    ) -> Algorithm:

        if algorithm == (
            RateLimitAlgorithm.FIXED_WINDOW
        ):
            return FixedWindowAlgorithm(
                clock=clock
            )
        if algorithm == (
            RateLimitAlgorithm.SLIDING_WINDOW
        ):
            return SlidingWindowAlgorithm(
                clock=clock
            )
        if algorithm == (
            RateLimitAlgorithm.TOKEN_BUCKET
        ):
            return TokenBucketAlgorithm(
                clock=clock
            )

        raise ValueError(
            f"Unsupported rate-limit algorithm: {algorithm}"
        )
        