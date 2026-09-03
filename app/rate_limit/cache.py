from abc import ABC,abstractmethod

class RuleCache(ABC):

    @abstractmethod
    async def get(
        self,
        key: str,
    ):
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        key: str,
        value,
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