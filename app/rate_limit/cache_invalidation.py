class RuleCacheInvalidationService:

    def __init__(self,cache_service,):
        self.cache_service = cache_service

    async def invalidate_tenant(
        self,
        *,
        tenant_id: int,
    ) -> int:

        return (
            await self.cache_service
            .invalidate_tenant(
                tenant_id=tenant_id
            )
        )