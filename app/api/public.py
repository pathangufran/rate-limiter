from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession 
from app.api.dependencies import get_api_key_identity
from app.core.auth import APIKeyIdentity
from app.db.session import get_db
from app.rate_limit.resolver import RateLimitResolver

router = APIRouter(
    prefix="/api/v1",
    tags=["Public"],
)

@router.get("/whoami")
async def who_am_i(
    identity: APIKeyIdentity = Depends(
        get_api_key_identity
    ),
):
    return {
        "api_key_id": str(identity.api_key_id),
        "tenant_id": str(identity.tenant_id),
        "user_id": (
            str(identity.user_id)
            if identity.user_id
            else None
        ),
    }

@router.get("/rate-limit-context")
async def get_rate_limit_context(
    request: Request,
    identity: APIKeyIdentity = Depends(
        get_api_key_identity
    ),
    session: AsyncSession = Depends(get_db),
):

    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    resolver = RateLimitResolver(session)
    context = await resolver.resolve(
        identity=identity,
        method=request.method,
        path=request.url.path,
        client_ip=client_ip,
    )
    return {
        "tenant_id": str(
            context.identity.tenant_id
        ),
        "api_key_id": (
            str(context.identity.api_key_id)
            if context.identity.api_key_id
            else None
        ),
        "user_id": (
            str(context.identity.user_id)
            if context.identity.user_id
            else None
        ),
        "client_ip": context.identity.client_ip,
        "method": context.request.method,
        "path": context.request.path,
        "endpoint_id": (
            str(context.endpoint_id)
            if context.endpoint_id
            else None
        ),
        "rules": [
            {
                "rule_id": str(
                    resolved.rule.id
                ),
                "scope": resolved.rule.scope,
                "priority": resolved.rule.priority,
                "policy_id": str(
                    resolved.policy.id
                ),
                "algorithm": resolved.policy.algorithm,
            }
            for resolved in context.rules
        ],
    }