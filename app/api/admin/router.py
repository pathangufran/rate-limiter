from fastapi import APIRouter
from app.api.admin.api_keys import (
    router as api_key_router
)
from app.api.admin.auth import (
    router as auth_router
)
from app.api.admin.endpoints import (
    router as endpoint_router
)
from app.api.admin.plan import (
    router as plan_router
)
from app.api.admin.policies import (
    router as policy_router
)
from app.api.admin.rules import (
    router as rule_router
)

router = APIRouter()

router.include_router(auth_router)
router.include_router(api_key_router)
router.include_router(plan_router)
router.include_router(endpoint_router)
router.include_router(policy_router)
router.include_router(rule_router)