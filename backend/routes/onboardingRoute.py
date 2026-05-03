import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.models.onboarding import (
    OnboardingQuestion,
    OnboardingResponse,
    UserMentalProfile,
)
from backend.schemas.onboardingSchema import (
    SubmitAnswerRequest,
    CompleteOnboardingResponse,
)
from backend.service.aiProfileService import generate_ai_profile

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.get("/questions")
def get_questions(db: Session = Depends(get_db)):
    questions = (
        db.query(OnboardingQuestion)
        .order_by(OnboardingQuestion.order_index)
        .all()
    )

    return [
        {
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "category": q.category,
            "options": json.loads(q.options_json),
            "order_index": q.order_index,
        }
        for q in questions
    ]


@router.post("/answer")
def submit_answer(data: SubmitAnswerRequest, db: Session = Depends(get_db)):
    question = (
        db.query(OnboardingQuestion)
        .filter(OnboardingQuestion.id == data.question_id)
        .first()
    )

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    old_answer = (
        db.query(OnboardingResponse)
        .filter(
            OnboardingResponse.user_id == data.user_id,
            OnboardingResponse.question_id == data.question_id,
        )
        .first()
    )

    answer_json = json.dumps(data.answer)

    if old_answer:
        old_answer.answer_json = answer_json
    else:
        new_answer = OnboardingResponse(
            user_id=data.user_id,
            question_id=data.question_id,
            answer_json=answer_json,
        )
        db.add(new_answer)

    db.commit()

    return {"message": "Answer saved successfully"}


@router.get("/responses/{user_id}")
def get_user_responses(user_id: int, db: Session = Depends(get_db)):
    responses = (
        db.query(OnboardingResponse, OnboardingQuestion)
        .join(OnboardingQuestion, OnboardingResponse.question_id == OnboardingQuestion.id)
        .filter(OnboardingResponse.user_id == user_id)
        .all()
    )

    return [
        {
            "question_id": question.id,
            "question": question.question_text,
            "answer": json.loads(response.answer_json),
        }
        for response, question in responses
    ]


@router.post("/complete/{user_id}", response_model=CompleteOnboardingResponse)
def complete_onboarding(user_id: int, db: Session = Depends(get_db)):
    responses = (
        db.query(OnboardingResponse, OnboardingQuestion)
        .join(OnboardingQuestion, OnboardingResponse.question_id == OnboardingQuestion.id)
        .filter(OnboardingResponse.user_id == user_id)
        .all()
    )

    if not responses:
        raise HTTPException(status_code=400, detail="No onboarding answers found")

    answers = {}
    pronouns = None
    age_group = None

    for response, question in responses:
        answer = json.loads(response.answer_json)
        answers[question.category] = answer

        if question.category == "pronouns":
            pronouns = answer

        if question.category == "age":
            age_group = answer

    profile_data = generate_ai_profile(answers)

    existing_profile = (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )

    if existing_profile:
        existing_profile.pronouns = pronouns
        existing_profile.age_group = age_group
        existing_profile.stress_score = profile_data["stress_score"]
        existing_profile.wellness_score = profile_data["wellness_score"]
        existing_profile.emotional_state = profile_data["emotional_state"]
        existing_profile.support_level = profile_data["support_level"]
        existing_profile.risk_level = profile_data["risk_level"]
        existing_profile.personality_summary = profile_data["personality_summary"]
    else:
        new_profile = UserMentalProfile(
            user_id=user_id,
            pronouns=pronouns,
            age_group=age_group,
            stress_score=profile_data["stress_score"],
            wellness_score=profile_data["wellness_score"],
            emotional_state=profile_data["emotional_state"],
            support_level=profile_data["support_level"],
            risk_level=profile_data["risk_level"],
            personality_summary=profile_data["personality_summary"],
        )
        db.add(new_profile)

    db.commit()

    return {
        "user_id": user_id,
        "wellness_score": profile_data["wellness_score"],
        "stress_score": profile_data["stress_score"],
        "emotional_state": profile_data["emotional_state"],
        "support_level": profile_data["support_level"],
        "risk_level": profile_data["risk_level"],
        "personality_summary": profile_data["personality_summary"],
        "message": "Your emotional wellness profile has been created successfully.",
    }


@router.get("/profile/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile