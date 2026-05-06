from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from backend.config.database import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)

    content = Column(Text, nullable=False)
    emotion = Column(String(100))
    confidence = Column(String(50))

    ai_summary = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())