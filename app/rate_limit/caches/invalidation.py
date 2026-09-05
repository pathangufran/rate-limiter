import logging
from app.rate_limit.rule_cache_service import RuleCacheService

logger = logging.getLogger(__name__)

class RuleCacheInvalidationService:

    def __init__(
        self,
        cache_service: RuleCacheService,
    ):
        self.cache_service = cache_service

    async def invalidate_tenant(
        self,
        *,
        tenant_id: int,
    ) -> int:
        """
        Invalidate all cached rate-limit rules
        belonging to a tenant.

        Uses tenant-level generation invalidation instead
        of deleting individual Redis keys.
        """

        try:
            new_generation = (
                await self.cache_service.invalidate_tenant(
                    tenant_id=tenant_id,
                )
            )
            logger.info(
                "Rate-limit rule cache invalidated",
                extra={
                    "tenant_id": tenant_id,
                    "generation": new_generation,
                },
            )

            return new_generation

        except Exception:
            logger.exception(
                "Failed to invalidate rate-limit rule cache",
                extra={
                    "tenant_id": tenant_id,
                },
            )
            raise