from pydantic import BaseModel
from typing import List, Union, Optional


class OnboardingQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    category: str
    options: List[str]
    order_index: int


class SubmitAnswerRequest(BaseModel):
    user_id: int
    question_id: int
    answer: Union[str, List[str]]


class CompleteOnboardingResponse(BaseModel):
    user_id: int
    wellness_score: int
    stress_score: int
    emotional_state: str
    support_level: str
    risk_level: str
    personality_summary: str
    message: str