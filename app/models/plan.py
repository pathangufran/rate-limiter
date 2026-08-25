from sqlalchemy import Boolean,String,Text
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.base import Base
from app.models.base import TimestampMixin

class Plan(TimestampMixin,Base):
    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    tenants = relationship(
        "Tenant",
        back_populates="plan",
    )