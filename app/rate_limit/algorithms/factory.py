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

    _algorithms: dict[RateLimitAlgorithm,type[Algorithm],] = {
        RateLimitAlgorithm.FIXED_WINDOW:
            FixedWindowAlgorithm,
        RateLimitAlgorithm.SLIDING_WINDOW:
            SlidingWindowAlgorithm,
        RateLimitAlgorithm.TOKEN_BUCKET:
            TokenBucketAlgorithm,
    }

    @classmethod
    def create(
        cls,
        algorithm: RateLimitAlgorithm,
    ) -> Algorithm:

        algorithm_class = cls._algorithms.get(
            algorithm
        )
        if algorithm_class is None:
            raise ValueError(
                f"Unsupported rate-limit algorithm: {algorithm}"
            )

        return algorithm_class()