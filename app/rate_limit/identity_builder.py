from uuid import UUID
from fastapi import Request
from app.rate_limit.context import RequestIdentity

def build_request_identity(
    request: Request,
) -> RequestIdentity:

    return RequestIdentity(
        tenant_id=get_state_uuid(
            request,
            "tenant_id",
        ),
        user_id=get_state_uuid(
            request,
            "user_id",
        ),
        api_key_id=get_state_uuid(
            request,
            "api_key_id",
        ),
        client_ip=(
            request.client.host
            if request.client
            else None
        )
    )

def get_state_uuid(
    request: Request,
    attribute: str,
) -> UUID | None:

    value = getattr(
        request.state,
        attribute,
        None,
    )
    if value is None:
        return None

    if isinstance(value,UUID):
        return value

    return UUID(str(value))