from uuid import UUID
from dataclasses import dataclass
from app.rate_limit.result import RateLimitResult

@dataclass(frozen=True)
class RuleEvaluationResult:
    ruld_id: UUID
    scope: str
    result: RateLimitResult

@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    evaluations: tuple[
        RuleEvaluationResult,
        ...
    ]

    rejected_rule_id: UUID | None = None