from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import AsyncSessionLocal
from app.redis.client import redis_client
from app.api.admin.router import router as admin_router
from app.api.public import router as public_router

router = APIRouter()

@router.get("/health",tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
    }

@router.get("/ready",tags=["Health"])
async def readiness_check():
    dependencies = {}

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))

        dependencies["postgres"] = "healthy"

    except Exception:
        dependencies["postgres"] = "unhealthy"

    try:
        await redis_client.ping()
        dependencies["redis"] = "healthy"

    except Exception:
        dependencies["redis"] = "unhealthy"

    ready = all(
        status == "healthy"
        for status in dependencies.values()
    )

    return {
        "status":"ready" if ready else "not_ready",
        "dependencies": dependencies,
    }

router.include_router(admin_router)
router.include_router(public_router)