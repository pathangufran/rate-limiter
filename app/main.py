from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(lambda _: None)

    yield

    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(router)