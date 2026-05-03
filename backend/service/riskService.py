from sqlalchemy.orm import Session
from backend.models.mood import Mood
from backend.models.chat import ChatHistory
from backend.models.onboarding import UserMentalProfile
from backend.ml.riskPrediction import predictRiskML


negativeEmotions = [
    "sadness", "grief", "fear", "nervousness",
    "remorse", "disappointment", "anger"
]

lowMoods = ["Low", "Overwhelmed"]


def calculateRiskScore(db: Session, user_id: int):
    score = 0
    reasons = []

    # 1. Onboarding profile
    profile = (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )

    stress_score = 50
    support_level = "medium"

    if profile:
        stress_score = profile.stress_score if profile.stress_score else 50
        support_level = profile.support_level if profile.support_level else "medium"

        if profile.risk_level == "High":
            score += 30
            reasons.append("High onboarding risk profile")

        if profile.stress_score and profile.stress_score >= 70:
            score += 25
            reasons.append("High stress score from onboarding")

        if profile.support_level == "Low support system":
            score += 20
            reasons.append("Low support system")

    # 2. Mood history
    moods = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.created_at.desc())
        .limit(7)
        .all()
    )

    lowMoodCount = sum(1 for mood in moods if mood.mood in lowMoods)

    if lowMoodCount >= 3:
        score += 25
        reasons.append("Repeated low mood check-ins")

    elif lowMoodCount >= 1:
        score += 10
        reasons.append("Recent low mood detected")

    # 3. Chat emotion history
    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(10)
        .all()
    )

    negativeEmotionCount = sum(
        1 for chat in chats if chat.emotion in negativeEmotions
    )

    if negativeEmotionCount >= 5:
        score += 30
        reasons.append("Frequent negative emotions in chat")

    elif negativeEmotionCount >= 2:
        score += 15
        reasons.append("Some negative emotional signals in chat")

    score = min(score, 100)

    if score >= 70:
        rule_level = "High"
    elif score >= 40:
        rule_level = "Medium"
    else:
        rule_level = "Low"

    # 🔥 ML PREDICTION (NEW)
    ml_risk = predictRiskML(
        stress_score,
        support_level,
        lowMoodCount,
        negativeEmotionCount
    )

    # 🔥 FINAL DECISION (combine both)
    final_risk = ml_risk  # you can later refine

    return {
        "user_id": user_id,
        "rule_score": score,
        "rule_level": rule_level,
        "ml_risk": ml_risk,
        "final_risk": final_risk,
        "reasons": reasons,
        "note": "AI-assisted risk prediction (not a medical diagnosis)"
    }