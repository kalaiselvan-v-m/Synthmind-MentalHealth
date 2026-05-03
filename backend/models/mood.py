from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.config.database import Base


class Mood(Base):
    __tablename__ = "moods"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    mood = Column(String(50), nullable=False)  # Happy / Normal / Low / Overwhelmed
    note = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())