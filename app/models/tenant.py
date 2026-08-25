import uuid
from sqlalchemy import ForeignKey,String,Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from app.models.base import TimestampMixin

class Tenant(TimestampMixin,Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plans.id"),
        nullable=False,
    )
    plan = relationship(
        "Plan",
        back_populates="tenants",
    )
    users = relationship(
        "User",
        back_populates="tenant",
    )
    api_keys = relationship(
        "APIKey",
        back_populates="tenant",
    )
