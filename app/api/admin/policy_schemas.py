from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel,Field,model_validator
from app.core.enums import RateLimitAlgorithm

class PolicyCreateRequest(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150,
    )
    description: str | None = Field(default=None,max_length=500,)

    algorithm: RateLimitAlgorithm

    request_limit: int | None = Field(default=None,gt=0,)
    window_seconds: int | None = Field(default=None,gt=0,)
    burst_capacity: int | None = Field(default=None,gt=0,)
    refill_rate: Decimal | None = Field(default=None,gt=0,)

    @model_validator(mode="after")
    def validate_algorithm_configuration(self):

        if self.algorithm in {
            RateLimitAlgorithm.FIXED_WINDOW,
            RateLimitAlgorithm.SLIDING_WINDOW,
        }:
            if self.request_limit is None:
                raise ValueError(
                    "request_limit is required for "
                    f"{self.algorithm}"
                )
            if self.window_seconds is None:
                raise ValueError(
                    "window_seconds is required for "
                    f"{self.algorithm}"
                )
            if self.burst_capacity is not None:
                raise ValueError(
                    "burst_capacity is not supported for "
                    f"{self.algorithm}"
                )
            if self.refill_rate is not None:
                raise ValueError(
                    "refill_rate is not supported for "
                    f"{self.algorithm}"
                )

        elif self.algorithm == RateLimitAlgorithm.TOKEN_BUCKET:
            if self.burst_capacity is None:
                raise ValueError(
                    "burst_capacity is required for TOKEN_BUCKET"
                )
            if self.refill_rate is None:
                raise ValueError(
                    "refill_rate is required for TOKEN_BUCKET"
                )
            if self.request_limit is not None:
                raise ValueError(
                    "request_limit is not supported for TOKEN_BUCKET"
                )
            if self.window_seconds is not None:
                raise ValueError(
                    "window_seconds is not supported for TOKEN_BUCKET"
                )

        return self

class PolicyUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    description: str | None = Field(default=None,max_length=500,)
    request_limit: int | None = Field(default=None,gt=0,)
    window_seconds: int | None = Field(default=None,gt=0,)
    burst_capacity: int | None = Field(default=None,gt=0,)
    refill_rate: Decimal | None = Field(default=None,gt=0,)
    is_active: bool | None = None

class PolicyResponse(BaseModel):
    id: UUID
    name: str
    description: str | None

    algorithm: RateLimitAlgorithm

    request_limit: int | None
    window_seconds: int | None
    burst_capacity: int | None
    refill_rate: Decimal | None
    is_active: bool

    model_config = {
        "from_attributes": True
    }