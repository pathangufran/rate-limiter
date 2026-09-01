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
    def _get_effective_evaluation(decision):

        if not decision.evaluation:
            return None

        return min(
            decision.evaluations,
            key=lambda evaluation: (
                evaluation.result.remaining
            ),
        )

    @staticmethod
    def _add_rate_limit_headers(
        response,
        decision,
    ) -> None:

        evaluation = (
            RateLimitMiddleware
            ._get_effective_evaluation(
                decision
            )
        )

        if evaluation is None:
            return

        result = evaluation.result

        response.headers[
            "X-RateLimit-Limit"
        ] = str(result.limit)

        response.headers[
            "X-RateLimit-Remaining"
        ] = str(result.remaining)

        response.headers[
            "X-RateLimit-Reset"
        ] = str(result.reset_after)


    @staticmethod
    def _build_rate_limit_response(
        decision,
    ) -> JSONResponse:

        response = JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "error": "rate_limit_exceeded",
                "rule_id": (
                    str(decision.rejected_rule_id)
                    if decision.rejected_rule_id
                    else None
                ),
            },
        )

        evaluation = next(
            (
                evaluation
                for evaluation in decision.evaluations
                if evaluation.rule_id
                == decision.rejected_rule_id
            ),
            None,
        )

        if evaluation is not None:

            result = evaluation.result

            response.headers[
                "X-RateLimit-Limit"
            ] = str(result.limit)

            response.headers[
                "X-RateLimit-Remaining"
            ] = str(result.remaining)

            if result.retry_after is not None:

                response.headers[
                    "Retry-After"
                ] = str(result.retry_after)

        return response
