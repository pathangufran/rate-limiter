from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import AsyncSessionLocal

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

    ready = all(
        status == "healthy"
        for status in dependencies.values()
    )

    return {
        "status":"ready" if ready else "not_ready",
        "dependencies": dependencies,
    }