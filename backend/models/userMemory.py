from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from backend.config.database import Base


class UserMemory(Base):
    __tablename__ = "user_memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)

    memory_type = Column(String(50), nullable=False)
    memory_key = Column(String(100), nullable=False)
    memory_value = Column(Text, nullable=False)

    importance = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())