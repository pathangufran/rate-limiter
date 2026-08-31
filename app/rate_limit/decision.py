from app.rate_limit.evaluation import (
    RateLimitDecision,
    RuleEvaluationResult,
)

def get_effective_evaluation(
    decision: RateLimitDecision,
) -> RuleEvaluationResult | None:

    if not decision.evaluations:
        return None

    return min(
        decision.evaluations,
        key=lambda evaluation: (
            evaluation.result.remaining
        ),
    )
