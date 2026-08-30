from app.core.enums import RateLimitAlgorithm
from app.models.rate_limit_policy import RateLimitPolicy
from app.rate_limit.policy import RateLimitPolicyConfig

def to_policy_config(
    policy: RateLimitPolicy,
) -> RateLimitPolicyConfig:

    return RateLimitPolicyConfig(
        id=policy.id,
        algorithm=RateLimitAlgorithm(
            policy.algorithm,
        ),
        request_limit=policy.request_limit,
        window_seconds=policy.window_seconds,
        burst_capacity=policy.burst_capacity,
        refill_rate=policy.refill_rate,
    )