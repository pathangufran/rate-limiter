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

def get_rejected_evaluation(
    decision: RateLimitDecision,
) -> RuleEvaluationResult | None:

    if decision.rejected_rule_id is None:
        return None

    for evaluation in (
        decision.evaluations
    ):
        if (
            evaluation.rule_id
            == decision.rejected_rule_id
        ):
            return evaluation

    return None