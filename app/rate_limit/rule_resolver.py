from fastapi import Request

class RuleResolver:

    async def resolve(
        self,
        *,
        method: str,
        path: str,
        identity,
    ) -> tuple:

        return ()