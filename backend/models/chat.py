from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from backend.config.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    mode = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    emotion = Column(String(100), nullable=True)
    confidence = Column(String(50), nullable=True)