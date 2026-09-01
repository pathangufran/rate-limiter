from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings
from app.redis.client import redis_client
from app.middleware.rate_limit import (
    RateLimitMiddleware,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.ping()
    yield
    await redis_client.aclose()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(router)
app.add_middleware(
    RateLimitMiddleware,
    rate_limit_engine="rate_limit_engine",
    rule_resolver="rule_resolver",
)