from fastapi import APIRouter
from app.api.admin.api_keys import (
    router as api_key_router
)
from app.api.admin.auth import (
    router as auth_router
)

router = APIRouter()

router.include_router(auth_router)
router.include_router(api_key_router)