from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.config.database import Base


class OnboardingQuestion(Base):
    __tablename__ = "onboarding_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # single_choice / multi_choice
    category = Column(String(100), nullable=False)
    options_json = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)


class OnboardingResponse(Base):
    __tablename__ = "onboarding_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("onboarding_questions.id"))
    answer_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserMentalProfile(Base):
    __tablename__ = "user_mental_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    pronouns = Column(String(50))
    age_group = Column(String(50))
    stress_score = Column(Integer, default=0)
    wellness_score = Column(Integer, default=0)
    emotional_state = Column(String(100))
    support_level = Column(String(100))
    risk_level = Column(String(100))
    personality_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())