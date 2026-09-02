from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from app.rate_limit.context import RateLimitContext
from app.rate_limit.identity_builder import (
    build_request_identity,
)
from app.rate_limit.rule_resolver import RuleResolver
from app.rate_limit.decision import (
    get_effective_evaluation,
    get_rejected_evaluation,
)
from app.rate_limit.http import (
    build_rate_limit_headers,
    build_rate_limit_response,
)

class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(
        self,
        app: ASGIApp,
        *,
        rate_limit_engine,
        rule_resolver: RuleResolver,
    ):
        super.__init__(app)

        self.rate_limit_engine = rate_limit_engine
        self.rule_resolver = rule_resolver

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ):
        if self._should_skip(request):
            return await call_next(request)

        identity = build_request_identity(request)

        rules = await (
            self.rule_resolver.resolve(
                method=request.method,
                path=request.url.path,
                identity=identity,
            )
        )

        if not rules:
            return await call_next(request)

        context = RateLimitContext(
            method=request.method,
            path=request.url.path,
            endpoint=request.url.path,
            identity=identity,
            rules=rules,
        )

        decision = (
            await self.rate_limit_engine.check(
                context
            )
        )
        if not decision.allowed:
            return self._build_rate_limit_response(
                decision
            )

        response = await call_next(request)

        self._add_rate_limit_headers(
            response,
            decision,
        )

        return response

    @staticmethod
    def _should_skip(
        request: Request,
    ) -> bool:

        excluded_paths = {
            "/health",
            "/health/",
            "/docs",
            "/docs/",
            "/openapi.json",
        }

        return request.url.path in (
            excluded_paths
        )

    @staticmethod
    def _build_rejection_response(
        decision,
    ):
        evaluation = (
            get_rejected_evaluation(decision)
        )

        if evaluation is None:
            return RuntimeError(
                "Rejected decision has no "
                "rejected evaluation"
            )

        return build_rate_limit_response(
            rule_id=(
                decision.rejected_rule_id
            ),
            result=evaluation.result,
        )

    @staticmethod
    def _add_success_headers(
        response,
        decision,
    ) -> None:

        evaluation = (
            get_effective_evaluation(decision)
        )

        if evaluation is None:
            return

        result = evaluation.result

        headers = build_rate_limit_headers(
            limit=result.limit,
            remaining=result.remaining,
            reset_after=result.reset_after,
        )

        for name,value in headers.items():

            response.headers[name] = value

        return response