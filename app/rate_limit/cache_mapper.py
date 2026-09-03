from app.rate_limit.cache_models import (
    CachedRule,
)

def rule_to_cached_rule(
    resolved_rule,
) -> CachedRule:

    rule = resolved_rule.rule
    policy = resolved_rule.policy

    return CachedRule(
        rule_id=int(rule.id),
        policy_id=int(policy.id),
        scope=str(rule.scope),
        identity_type=str(
            rule.identity_type
        ),
        priority=int(rule.priority),
        algorithm=str(
            policy.algorithm
        ),
        request_limit=int(
            policy.request_limit
        ),
        window_seconds=(
            int(policy.window_seconds)
            if policy.window_seconds is not None
            else None
        ),
        burst_capacity=(
            int(policy.burst_capacity)
            if policy.burst_capacity is not None
            else None
        ),
        refill_rate=(
            float(policy.refill_rate)
            if policy.refill_rate is not None
            else None
        ),
    )