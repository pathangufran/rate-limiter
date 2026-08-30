from dataclasses import dataclass
from uuid import UUID
from app.models.rate_limit_policy import RateLimitPolicy
from app.models.rate_limit_rule import RateLimitRule

@dataclass(frozen=True)
class RequestIdentity:
    tenant_id: UUID
    api_key_id: UUID | None
    user_id: UUID | None
    client_ip: str

@dataclass(frozen=True)
class RateLimitRequest:
    method: str
    path: str

@dataclass(frozen=True)
class ResolvedRule:
    rule: RateLimitRule
    policy: RateLimitPolicy

@dataclass(frozen=True)
class RateLimitContext:
    identity: RequestIdentity
    request: RateLimitRequest
    endpoint_id: UUID | None
    rules: tuple[ResolvedRule,...]