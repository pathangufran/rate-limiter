import pytest
from app.redis.client import redis_client

@pytest.mark.asyncio
async def test_redis_connection():
    response = await redis_client.ping()

    assert response is True