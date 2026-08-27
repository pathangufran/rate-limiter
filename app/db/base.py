from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.models import (
    api_key,
    audit_log,
    endpoint,
    plan,
    rate_limit_policy,
    rate_limit_rule,
    tenant,
    user,
)