
from sqlalchemy.orm import Session

from backend.models.crisisEvent import CrisisEvent
from backend.models.chat import ChatHistory


CRITICAL_PHRASES = [
    "kill myself",
    "end my life",
    "i want to die",
    "i don't want to live",
    "i dont want to live",
    "suicide",
    "hurt myself",
    "self harm",
    "self-harm"
]

HIGH_RISK_PHRASES = [
    "i can't do this anymore",
    "i cant do this anymore",
    "i feel hopeless",
    "nothing matters",
    "i want everything to stop",
    "i feel empty",
    "i'm done",
    "im done"
]

MEDIUM_RISK_PHRASES = [
    "overwhelmed",
    "panic",
    "very scared",
    "breaking down",
    "can't breathe",
    "cant breathe",
    "too much pressure"
]

NEGATIVE_EMOTIONS = [
    "fear",
    "sadness",
    "grief",
    "nervousness",
    "anger"
]


def classifyCrisis(message: str, recent_negative_count: int = 0):

    msg = message.lower().strip()

    # 1. Critical risk
    for phrase in CRITICAL_PHRASES:

        if phrase in msg:
            return {
                "crisis_detected": True,
                "risk_level": "CRITICAL",
                "reason": (
                    f"Critical self-harm phrase detected: {phrase}"
                )
            }

    # 2. High risk
    for phrase in HIGH_RISK_PHRASES:

        if phrase in msg:
            return {
                "crisis_detected": True,
                "risk_level": "HIGH",
                "reason": (
                    f"High-risk hopelessness phrase detected: {phrase}"
                )
            }

    # 3. Medium distress
    for phrase in MEDIUM_RISK_PHRASES:

        if phrase in msg:
            return {
                "crisis_detected": False,
                "risk_level": "MEDIUM",
                "reason": (
                    f"Medium distress phrase detected: {phrase}"
                )
            }

    # 4. Repeated negative emotional history
    if recent_negative_count >= 4:

        return {
            "crisis_detected": False,
            "risk_level": "MEDIUM",
            "reason": "Repeated recent negative emotions"
        }

    # 5. Normal condition
    return {
        "crisis_detected": False,
        "risk_level": "LOW",
        "reason": "No crisis pattern detected"
    }


def getRecentNegativeCount(
    db: Session,
    user_id: int,
    limit: int = 8
):

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    return sum(
        1 for chat in chats
        if chat.emotion in NEGATIVE_EMOTIONS
    )


def buildCrisisResponse(risk_level: str):

    if risk_level == "CRITICAL":

        return (
            "I'm really sorry you're experiencing this. "
            "Please contact someone you trust right now "
            "and seek immediate emergency support if you may "
            "act on these thoughts. Stay with a trusted person "
            "and move away from anything you could use to hurt yourself."
        )

    if risk_level == "HIGH":

        return (
            "I'm here to listen. This sounds very difficult. "
            "Please reach out to someone you trust today. "
            "You do not have to manage this alone."
        )

    if risk_level == "MEDIUM":

        return (
            "It sounds like you're under pressure. "
            "Let's slow down for a moment. Take a gentle breath "
            "and focus on one manageable next step."
        )

    return ""


def analyzeCrisis(
    db: Session,
    user_id: int,
    message: str
):

    recent_negative_count = getRecentNegativeCount(
        db,
        user_id
    )

    result = classifyCrisis(
        message,
        recent_negative_count
    )

    response = buildCrisisResponse(
        result["risk_level"]
    )

    # Save medium, high and critical support events.
    if result["risk_level"] in [
        "MEDIUM",
        "HIGH",
        "CRITICAL"
    ]:

        event = CrisisEvent(
            user_id=user_id,
            message=message,
            risk_level=result["risk_level"],
            reason=result["reason"],
            response=response,
            crisis_detected=result["crisis_detected"]
        )

        db.add(event)
        db.commit()
        db.refresh(event)

    return {
        **result,
        "response": response
    }
