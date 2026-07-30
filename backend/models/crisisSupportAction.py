from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text
)

from sqlalchemy.sql import func

from backend.config.database import Base


class CrisisSupportAction(Base):
    __tablename__ = "crisis_support_actions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    risk_level = Column(
        String(50),
        nullable=True
    )

    action_type = Column(
        String(100),
        nullable=False
    )
    # trusted_contact_preview
    # trusted_contact_requested
    # grounding_requested

    status = Column(
        String(50),
        default="pending"
    )

    details = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )