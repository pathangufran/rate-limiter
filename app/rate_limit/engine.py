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

class RateLimitEngine:

    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    async def check(
        self,
        context: RateLimitContext,
    ) -> tuple[RateLimitResult,...]:

        results = list[RateLimitResult] = []
        for resolved_rule in context.rules:
            policy = to_policy_config(
                resolved_rule.policy
            )
            algorithm = AlgorithmFactory.create(
                policy.algorithm
            )
            identity_type = (
                self._identity_type(
                    resolved_rule.rule.scope
                )
            )
            identity_key = build_identity_key(
                api_key_id=(
                    context.identity.api_key_id
                ),
                user_id=(
                    context.identity.user_id
                ),
                tenant_id=(
                    context.identity.tenant_id
                ),
                client_ip=(
                    context.identity.client_ip
                ),
                identity_type=identity_type,
            )

            timestamp = current_timestamp()

            key = self._build_state_key(
                algorithm_name=policy.algorithm.value,
                rule_id=resolved_rule.rule.id,
                identity_key=identity_key,
                policy=policy,
                timestamp=timestamp,
            )
            result = await algorithm.check(
                redis=self.redis,
                key=key,
                policy=policy,
            )

            results.append(result)

            if not result.allowed:
                break

        return tuple(results)

    @staticmethod
    def _identity_type(
        scope: str,
    ) -> str:
        mapping = {
            "GLOBAL": "global",
            "PLAN": "tenant",
            "TENANT": "tenant",
            "USER": "user",
            "API_KEY": "api_key",
            "IP": "ip",
            "ENDPOINT": "api_key",
        }

        try:
            return mapping[scope]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported rule scope: {scope}"
            ) from exc

    @staticmethod
    def _build_state_key(
        *,
        algorithm_name: str,
        rule_id,
        identity_key: str,
        policy,
        timestamp: int,
    ) -> str:

        if algorithm_name == "FIXED_WINDOW":
            if policy.window_seconds is None:
                raise ValueError(
                    "window_seconds is required"
                )

            window_number = get_window_number(
                timestamp,
                policy.window_seconds,
            )
            
            return build_fixed_window_key(
                rule_id=rule_id,
                identity_key=identity_key,
                window_number=window_number,
            )

        return (
            f"rl:state:"
            f"{algorithm_name.lower()}:"
            f"{rule_id}:"
            f"{identity_key}"
        )

        