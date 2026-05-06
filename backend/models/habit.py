from sqlalchemy import Column, Integer, String, Text, DateTime, Date, UniqueConstraint
from sqlalchemy.sql import func
from backend.config.database import Base


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    habit_title = Column(String(200), nullable=False)
    habit_category = Column(String(100), nullable=True)
    completed_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "habit_title", "completed_date", name="unique_daily_habit_completion"),
    )