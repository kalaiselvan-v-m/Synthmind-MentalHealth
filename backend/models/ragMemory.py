from sqlalchemy import Column, Integer, Text, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from backend.config.database import Base


class RagMemory(Base):
    __tablename__ = "rag_memories"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    content = Column(Text, nullable=False)

    embedding = Column(JSONB, nullable=False)

    emotion = Column(Text, default="neutral")

    importance = Column(Float, default=0.3)

    created_at = Column(DateTime(timezone=True), server_default=func.now())