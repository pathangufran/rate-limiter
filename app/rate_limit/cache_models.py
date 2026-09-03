from dataclasses import asdict,dataclass
from typing import Any

@dataclass(frozen=True)
class CachedRule:
    """
    Serializable representation of a resolved
    rate-limit rule.

    This object is intentionally independent
    of SQLAlchemy/database models.
    """
    rule_id: int
    policy_id: int
    scope: str
    identity_type: str
    priority: int

    algorithm: str
    request_limit: int
    window_seconds: int | None
    burst_capacity: int | None
    refill_rate: int | None

    def to_dict(self) -> dict[str,Any]:
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: dict[str,Any],
    ) -> "CachedRule":

        return cls(
            rule_id=int(data["rule_id"]),
            policy_id=int(data["policy_id"]),
            scope=data["scope"],
            identity_type=data["identity_type"],
            priority=int(data["priority"]),
            algorithm=data["algorithm"],
            request_limit=int(
                data["request_limit"]
            ),
            window_seconds=(
                int(data["window_seconds"])
                if data["window_seconds"] is not None
                else None
            ),
            burst_capacity=(
                int(data["burst_capacity"])
                if data["burst_capacity"] is not None
                else None
            ),
            refill_rate=(
                float(data["refill_rate"])
                if data["refill_rate"] is not None
                else None
            ),
        )
