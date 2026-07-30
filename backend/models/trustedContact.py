from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from backend.config.database import Base


class TrustedContact(Base):
    __tablename__ = "trusted_contacts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    contact_name = Column(
        String(120),
        nullable=False
    )

    contact_phone = Column(
        String(30),
        nullable=True
    )

    contact_email = Column(
        String(150),
        nullable=True
    )

    relationship = Column(
        String(80),
        nullable=True
    )

    alerts_enabled = Column(
        Boolean,
        default=True
    )

    notify_on_critical = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )