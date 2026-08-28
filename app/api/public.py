from fastapi import APIRouter, Depends
from app.api.dependencies import get_api_key_identity
from app.core.auth import APIKeyIdentity

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