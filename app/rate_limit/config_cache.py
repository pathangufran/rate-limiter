import json
from uuid import UUID
from redis.asyncio import Redis
from app.models.rate_limit_policy import RateLimitPolicy
from app.models.rate_limit_rule import RateLimitRule

class RateLimitConfigCache:

    GLOBAL_KEY = "rl:config:global"

    def __init__(self,redis: Redis,):
        self.redis = redis

    @staticmethod
    def policy_to_dict(
        policy: RateLimitPolicy,
    ) -> dict:

        return {
            "id": str(policy.id),
            "name": policy.name,
            "algorithm": policy.algorithm,
            "request_limit": policy.request_limit,
            "window_seconds": policy.window_seconds,
            "burst_capacity": policy.burst_capacity,
            "refill_rate": (
                str(policy.refill_rate)
                if policy.refill_rate is not None
                else None
            ),
            "is_active": policy.is_active,
        }

    @classmethod
    def rule_to_dict(
        cls,
        rule: RateLimitRule,
    ) -> dict:

        return {
            "id": str(rule.id),
            "policy_id": str(rule.policy_id),
            "scope": rule.scope,
            "plan_id": (
                str(rule.plan_id)
                if rule.plan_id
                else None
            ),
            "tenant_id": (
                str(rule.tenant_id)
                if rule.tenant_id
                else None
            ),
            "user_id": (
                str(rule.user_id)
                if rule.user_id
                else None
            ),
            "api_key_id": (
                str(rule.api_key_id)
                if rule.api_key_id
                else None
            ),
            "endpoint_id": (
                str(rule.endpoint_id)
                if rule.endpoint_id
                else None
            ),
            "priority": rule.priority,
            "is_active": rule.is_active,
            "policy": (
                cls.policy_to_dict(rule.policy)
                if rule.policy
                else None
            ),
        }

    async def set(
        self,
        key: str,
        rules: list[RateLimitRule],
    ) -> None:

        payload = {
            "rules": [
                self.rule_to_dict(rule)
                for rule in rules
            ]
        }

        await self.redis.set(
            key,
            json.dumps(payload),
        )

    async def get(self,key: str,) -> dict | None:

        value = await self.redis.get(key)
        if value is None:
            return None

        return json.loads(value)

    async def delete(self,key: str,) -> None:

        await self.redis.delete(key)