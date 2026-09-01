from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from app.auth.exceptions import (
    InvalidAPIKeyError,
)
from app.auth.api_key import API_KEY_HEADER
class AuthenticationMiddleware(
    BaseHTTPMiddleware
):

    def __init__(
        self,
        *,
        app: ASGIApp,
        authentication_service,
    ): 
        super.__init__(app)
        self.authentication_service = (
            authentication_service
        )

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ):
        api_key = request.headers.get(
            API_KEY_HEADER
        )
        if api_key is None:

            return JSONResponse(
                status_code=401,
                content={
                    "detail": (
                        "Authentication required"
                    ),
                    "error": (
                        "authentication_required"
                    ),
                },   
            )

        try:
            identity = (
                await self
                .authentication_service
                .authenticate_api_key(api_key)
            )

        except InvalidAPIKeyError:

            return JSONResponse(
                status_code=401,
                content={
                    "detail": (
                        "Invalid API key"
                    ),
                    "error": (
                        "invalid_api_key"
                    ),
                },
            )

        request.state.api_key_id = (
            identity.api_key_id
        )
        request.state.user_id = (
            identity.user_id
        )
        request.state.tenant_id = (
            identity.tenant_id
        )

        return await call_next(request)
        
    