from uuid import UUID
from pydantic import BaseModel,Field,model_validator
from app.core.enums import RuleScope

class RuleCreateRequest(BaseModel):
    policy_id: UUID
    scope: RuleScope
    plan_id: UUID | None = None
    tenant_id: UUID | None = None
    user_id: UUID | None = None
    api_key_id: UUID | None = None
    endpoint_id: UUID | None = None

    priority: int = Field(
        default=0,
        ge=0,
        le=1000,
    )

    @model_validator(mode="after")
    def validate_scope(self):

        values = {
            RuleScope.GLOBAL: None,
            RuleScope.PLAN: self.plan_id,
            RuleScope.TENANT: self.tenant_id,
            RuleScope.USER: self.user_id,
            RuleScope.API_KEY: self.api_key_id,
            RuleScope.ENDPOINT: self.endpoint_id,
        }

        if self.scope == RuleScope.IP:
            if any(values.values()):
                raise ValueError(
                     "IP scope cannot contain database identity IDs"
                )
            return self

        if self.scope == RuleScope.GLOBAL:
            if any(values.values()):
                raise ValueError(
                    "GLOBAL scope cannot contain target IDs"
                )
            return self

        target_id = values[self.scope]
        if target_id is None:
            raise ValueError(
                f"{self.scope} scope requires its corresponding ID"
            )
        for scope,value in values.items():
            if scope != self.scope and value is not None:
                raise ValueError(
                    f"{self.scope} scope cannot contain {scope} ID"
                )

        return self


class RuleUpdateRequest(BaseModel):
    policy_id: UUID | None = None
    priority: int | None = Field(
        default=None,
        ge=0,
        le=1000,
    )
    is_active: bool | None = None

class RuleResponse(BaseModel):
    id: UUID
    policy_id: UUID
    score: RuleScope
    plan_id: UUID | None
    tenant_id: UUID | None
    user_id: UUID | None
    api_key_id: UUID | None
    endpoint_id: UUID | None
    priority: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }