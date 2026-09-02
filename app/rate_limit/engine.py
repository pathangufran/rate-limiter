from app.core.clock import Clock
from redis.asyncio import Redis
from app.rate_limit.algorithms.factory import (
    AlgorithmFactory,
)
from app.rate_limit.context import RateLimitContext
from app.rate_limit.keys import build_identity_key
from app.rate_limit.policy_mapper import to_policy_config
from app.rate_limit.result import RateLimitResult
from app.rate_limit.state import build_fixed_window_key
from app.rate_limit.time import (
    current_timestamp,
    get_window_number,
)
from app.rate_limit.evaluation import (
    RateLimitDecision,
    RuleEvaluationResult,
)
from app.rate_limit.identity import IdentityResolver
from app.rate_limit.policy import RateLimitPolicyConfig
from app.rate_limit.exceptions import (
    RateLimitError,     
)

class RateLimitEngine:

    def __init__(
        self,
        redis: Redis,
        clock: Clock,
        identity_resolver: IdentityResolver,
    ):
        self.redis = redis
        self.clock = clock
        self.identity_resolver = identity_resolver

    async def check(
        self,
        context: RateLimitContext,
    ) -> RateLimitDecision:

        evaluations = list[
            RuleEvaluationResult
        ] = []

        rules = sorted(
            context.rules,
            key=lambda resolved_rule: (
                resolved_rule.rule.priority
            ),
        )

        for resolved_rule in rules:
            rule = resolved_rule.rule
            policy = resolved_rule.policy

            identity_key = (
                self.identity_resolver.resolve(
                    context=context,
                    identity_type=rule.identity_type,
                    endpoint=context.endpoint,
                )
            )
            policy_config = (
                self._build_policy_config(policy)
            )
            algorithm = AlgorithmFactory.create(
                algorithm=policy_config.algorithm,
                clock=self.clock,
            )
            try:
                result = await algorithm.check(
                    redis=self.redis,
                    rule_id=rule.id,
                    identity_key=identity_key,
                    policy=policy_config,
                )

            except RateLimitError:
                raise

            evaluation = RuleEvaluationResult(
                rule_id=rule.id,
                scope=rule.scope,
                result=result,
            )
            evaluations.append(evaluation)

            if not result.allowed:

                return RateLimitDecision(
                    allowed=False,
                    evaluations=tuple(
                        evaluations
                    ),
                    rejected_rule_id=rule.id,
                )

        return RateLimitDecision(
            allowed=True,
            evaluations=tuple(
                evaluations
            ),
            rejected_rule_id=None,
        )

    @staticmethod
    def _build_policy_config(
        policy,
    ) -> RateLimitPolicyConfig:

        return RateLimitPolicyConfig(
            id=policy.id,
            algorithm=policy.algorithm,
            request_limit=policy.request_limit,
            window_seconds=policy.window_seconds,
            burst_capacity=policy.burst_capacity,
            refill_rate=policy.refill_rate,
        )


        