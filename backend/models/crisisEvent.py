from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean
)

from sqlalchemy.sql import func

from backend.config.database import Base


class CrisisEvent(Base):
    __tablename__ = "crisis_events"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    message = Column(
        Text,
        nullable=False
    )

    risk_level = Column(
        String(50),
        nullable=False
    )

    reason = Column(
        Text,
        nullable=True
    )

    response = Column(
        Text,
        nullable=True
    )

    crisis_detected = Column(
        Boolean,
        default=False
    )

    # -----------------------------
    # RECOVERY TRACKING
    # -----------------------------
    recovery_status = Column(
        String(50),
        default="active"
    )
    # active / stabilizing / recovered / worsening

    follow_up_needed = Column(
        Boolean,
        default=True
    )

    follow_up_message = Column(
        Text,
        nullable=True
    )

    resolved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )