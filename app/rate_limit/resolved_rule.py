from dataclasses import dataclass
from app.rate_limit.cache_models import (
    CachedRule,
)

@dataclass(frozen=True)
class CachedPolicy:
    id: int
    algorithm: str
    request_limit: int
    window_seconds: int | None
    burst_capacity: int | None
    refill_rate: float | None

@dataclass(frozen=True)
class CachedRuleDefinition:
    id: int
    scope: str
    identity_type: str
    priority: int

@dataclass(frozen=True)
class ResolvedCachedRule:
    rule: CachedRuleDefinition
    policy: CachedPolicy

def cached_rule_to_resolved_rule(
    cached: CachedRule,
) -> ResolvedCachedRule:

    return ResolvedCachedRule(
        rule=CachedRuleDefinition(
            id=cached.rule_id,
            scope=cached.scope,
            identity_type=cached.identity_type,
            priority=cached.priority,
        ),
        policy=CachedPolicy(
            id=cached.policy_id,
            algorithm=cached.algorithm,
            request_limit=cached.request_limit,
            window_seconds=(
                cached.window_seconds
            ),
            burst_capacity=(
                cached.burst_capacity
            ),
            refill_rate=(
                cached.refill_rate
            ),
        ),
    )
