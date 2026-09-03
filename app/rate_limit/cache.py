from abc import ABC,abstractmethod
from app.rate_limit.cache_models import (
    CachedRule,
)

class RuleCache(ABC):

    @abstractmethod
    async def get(
        self,
        key: str,
    ) -> list[CachedRule] | None:
        
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        key: str,
        rules: list[CachedRule],
        *,
        ttle: int,
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        key: str,
    ) -> None:
        raise NotImplementedError