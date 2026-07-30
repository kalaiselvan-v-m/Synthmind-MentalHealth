from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.models.crisisEvent import CrisisEvent
from backend.models.chat import ChatHistory


NEGATIVE_EMOTIONS = [
    "fear",
    "sadness",
    "grief",
    "nervousness",
    "anger",
    "remorse",
    "disappointment"
]

POSITIVE_EMOTIONS = [
    "joy",
    "relief",
    "gratitude",
    "calm",
    "optimism",
    "love"
]


def getLatestActiveCrisis(db: Session, user_id: int):
    return (
        db.query(CrisisEvent)
        .filter(CrisisEvent.user_id == user_id)
        .filter(CrisisEvent.recovery_status.in_(["active", "worsening", "stabilizing"]))
        .order_by(CrisisEvent.created_at.desc())
        .first()
    )


def getChatsAfterCrisis(db: Session, user_id: int, crisis_time):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .filter(ChatHistory.created_at >= crisis_time)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )


def analyzeRecoveryTrend(chats):
    if not chats:
        return {
            "status": "active",
            "reason": "No follow-up chat data yet."
        }

    recent = chats[-5:]

    negativeCount = 0
    positiveCount = 0

    for chat in recent:
        if chat.emotion in NEGATIVE_EMOTIONS:
            negativeCount += 1

        if chat.emotion in POSITIVE_EMOTIONS:
            positiveCount += 1

    if negativeCount >= 4:
        return {
            "status": "worsening",
            "reason": "Recent conversations still show repeated heavy emotions."
        }

    if positiveCount >= 2 and negativeCount <= 1:
        return {
            "status": "recovered",
            "reason": "Recent conversations show calmer or more positive signals."
        }

    if negativeCount <= 2:
        return {
            "status": "stabilizing",
            "reason": "Recent conversations look less emotionally intense."
        }

    return {
        "status": "active",
        "reason": "Recovery is still unclear."
    }


def buildFollowUpMessage(status: str):
    if status == "worsening":
        return (
            "You’ve seemed like things may still feel heavy. "
            "Can we slow down for a moment and focus on staying safe right now?"
        )

    if status == "stabilizing":
        return (
            "You seem a little steadier than earlier. "
            "Do you want to keep things gentle for a bit?"
        )

    if status == "recovered":
        return (
            "You seem a little more settled now. "
            "I’m glad you stayed through that moment."
        )

    return (
        "Hey… how are you feeling compared to earlier?"
    )


def updateRecoveryStatus(db: Session, user_id: int):
    crisis = getLatestActiveCrisis(db, user_id)

    if not crisis:
        return {
            "hasActiveRecovery": False,
            "message": None
        }

    chats = getChatsAfterCrisis(
        db,
        user_id,
        crisis.created_at
    )

    trend = analyzeRecoveryTrend(chats)

    crisis.recovery_status = trend["status"]
    crisis.follow_up_message = buildFollowUpMessage(trend["status"])

    if trend["status"] == "recovered":
        crisis.follow_up_needed = False
        crisis.resolved_at = datetime.utcnow()
    else:
        crisis.follow_up_needed = True

    db.commit()
    db.refresh(crisis)

    return {
        "hasActiveRecovery": True,
        "recoveryStatus": crisis.recovery_status,
        "followUpNeeded": crisis.follow_up_needed,
        "followUpMessage": crisis.follow_up_message,
        "reason": trend["reason"]
    }


def getRecoveryOverview(db: Session, user_id: int):
    crisis = getLatestActiveCrisis(db, user_id)

    if not crisis:
        return {
            "hasActiveRecovery": False,
            "recoveryStatus": "none",
            "message": "No active recovery check-in needed."
        }

    return {
        "hasActiveRecovery": True,
        "recoveryStatus": crisis.recovery_status,
        "followUpNeeded": crisis.follow_up_needed,
        "followUpMessage": crisis.follow_up_message or buildFollowUpMessage(crisis.recovery_status),
        "riskLevel": crisis.risk_level,
        "createdAt": crisis.created_at
    }