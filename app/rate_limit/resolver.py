from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import APIKeyIdentity
from app.rate_limit.context import (
    RateLimitContext,
    RateLimitRequest,
    RequestIdentity,
    ResolvedRule,
)
from app.rate_limit.endpoint_resolver import (
    EndpointResolver,
)
from app.repositories.rule_repository import (
    RuleRepository,
)
from app.repositories.tenant_repository import (
    TenantRepository,
)

class RateLimitResolver:

    def __init__(self,session: AsyncSession,):
        self.session = session
        self.rule_repository = RuleRepository(
            session
        )
        self.tenant_repository = TenantRepository(
            session
        )
        self.endpoint_resolver = EndpointResolver(
            session
        )

    async def resolve(
        self,
        *,
        identity: APIKeyIdentity,
        method: str,
        path: str,
        client_ip: str,
    ) -> RateLimitContext:

        tenant = await self.tenant_repository.get_by_id(
            identity.tenant_id
        )
        if tenant is None:
            raise ValueError(
                "Tenant associated with API key does not exist"
            )

        endpoint = await self.endpoint_resolver.resolve(
            method=method,
            path=path,
        )

        rules = await self.rule_repository.find_applicable(
            tenant_id=identity.tenant_id,
            plan_id=tenant.plan_id,
            user_id=identity.user_id,
            api_key_id=identity.api_key_id,
            endpoint_id=(
                endpoint.id
                if endpoint
                else None
            ),
        )
        resolved_rules = tuple(
            ResolvedRule(
                rule=rule,
                policy=rule.policy,
            )
            for rule in rules
            if rule.policy is not None
            and rule.policy.is_active
        )

        return RateLimitContext(
            identity=RequestIdentity(
                tenant_id=identity.tenant_id,
                api_key_id=identity.api_key_id,
                user_id=identity.user_id,
                client_ip=client_ip,
            ),
            request=RateLimitRequest(
                method=method.upper(),
                path=path,
            ),
            endpoint_id=(
                endpoint.id
                if endpoint
                else None
            ),
            rules=resolved_rules,
        )
    
