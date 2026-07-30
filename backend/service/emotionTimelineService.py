from sqlalchemy.orm import Session
from collections import Counter
from datetime import datetime, timedelta
from collections import defaultdict

from backend.models.chat import ChatHistory
from backend.models.mood import Mood
from backend.models.crisisEvent import CrisisEvent

# -------------------------------
# 🔹 GET LAST N DAYS EMOTIONS
# -------------------------------
def getEmotionTimeline(db: Session, user_id: int, days: int = 7):
    since = datetime.utcnow() - timedelta(days=days)

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .filter(ChatHistory.created_at >= since)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    return chats


# -------------------------------
# 🔹 DOMINANT EMOTION
# -------------------------------
def getDominantEmotion(chats):
    emotions = [chat.emotion for chat in chats if chat.emotion]

    if not emotions:
        return "neutral"

    return Counter(emotions).most_common(1)[0][0]


# -------------------------------
# 🔹 DETECT NEGATIVE STREAK
# -------------------------------
def detectNegativeStreak(chats):
    negativeEmotions = [
        "fear",
        "sadness",
        "grief",
        "nervousness",
        "remorse",
        "disappointment",
        "anger",
    ]

    streak = 0

    for chat in reversed(chats):
        if chat.emotion in negativeEmotions:
            streak += 1
        else:
            break

    return streak


# -------------------------------
# 🔹 DETECT IMPROVEMENT
# -------------------------------
def detectImprovement(chats):
    if len(chats) < 5:
        return False

    recent = chats[-5:]

    negativeEmotions = [
        "fear",
        "sadness",
        "grief",
        "nervousness",
        "remorse",
        "disappointment",
        "anger",
    ]

    positiveEmotions = [
        "joy",
        "calm",
        "relief",
        "gratitude",
        "optimism",
        "love",
    ]

    negative = 0
    positive = 0

    for chat in recent:
        if chat.emotion in negativeEmotions:
            negative += 1

        if chat.emotion in positiveEmotions:
            positive += 1

    return positive > negative


# -------------------------------
# 🔹 DETECT EMOTIONAL THEMES
# -------------------------------
def detectEmotionalThemes(chats):
    lonelinessKeywords = [
        "alone",
        "lonely",
        "invisible",
        "nobody cares",
        "no one cares",
        "not important",
        "worthless",
        "not worthy",
        "dont feel worthy",
        "don't feel worthy",
        "no friend",
        "no friends",
    ]

    exhaustionKeywords = [
        "tired",
        "exhausted",
        "drained",
        "burned out",
        "burnt out",
        "overwhelmed",
        "mentally tired",
        "can't do this",
        "cant do this",
        "fed up",
    ]

    selfDoubtKeywords = [
        "failed",
        "failure",
        "not good enough",
        "useless",
        "i can't",
        "i cant",
        "losing myself",
        "loosing myself",
        "hate myself",
        "not myself",
    ]

    lonelinessCount = 0
    exhaustionCount = 0
    selfDoubtCount = 0

    for chat in chats:
        msg = (chat.message or "").lower()

        if any(word in msg for word in lonelinessKeywords):
            lonelinessCount += 1

        if any(word in msg for word in exhaustionKeywords):
            exhaustionCount += 1

        if any(word in msg for word in selfDoubtKeywords):
            selfDoubtCount += 1

    return {
        "lonelinessCount": lonelinessCount,
        "exhaustionCount": exhaustionCount,
        "selfDoubtCount": selfDoubtCount,
    }


# -------------------------------
# 🔹 BUILD TIMELINE SUMMARY
# -------------------------------
def buildEmotionTimelineSummary(db: Session, user_id: int):
    chats = getEmotionTimeline(db, user_id)

    if not chats:
        return "No emotional history available."

    dominant = getDominantEmotion(chats)
    streak = detectNegativeStreak(chats)
    improving = detectImprovement(chats)
    themes = detectEmotionalThemes(chats)

    summary = f"""
Emotional Timeline:
- Dominant emotion: {dominant}
- Negative streak: {streak}
- Improving: {improving}
- Loneliness mentions: {themes["lonelinessCount"]}
- Exhaustion mentions: {themes["exhaustionCount"]}
- Self-doubt mentions: {themes["selfDoubtCount"]}
"""

    return summary

# -------------------------------
# 🔹 BUILD VISUAL EMOTION TIMELINE
# -------------------------------
def buildVisualEmotionTimeline(db: Session, user_id: int):
    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    moods = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.created_at.asc())
        .all()
    )

    crises = (
        db.query(CrisisEvent)
        .filter(CrisisEvent.user_id == user_id)
        .order_by(CrisisEvent.created_at.asc())
        .all()
    )

    grouped = defaultdict(lambda: {
        "date": "",
        "dominantEmotion": "neutral",
        "mood": None,
        "riskLevel": "LOW",
        "recoveryStatus": None,
        "events": []
    })

    for chat in chats:
        if not chat.created_at:
            continue

        dateKey = chat.created_at.strftime("%Y-%m-%d")
        grouped[dateKey]["date"] = dateKey

        if chat.emotion:
            grouped[dateKey]["dominantEmotion"] = chat.emotion

        grouped[dateKey]["events"].append({
            "type": "chat",
            "emotion": chat.emotion,
            "time": str(chat.created_at)
        })

    for mood in moods:
        if not mood.created_at:
            continue

        dateKey = mood.created_at.strftime("%Y-%m-%d")
        grouped[dateKey]["date"] = dateKey
        grouped[dateKey]["mood"] = mood.mood

        grouped[dateKey]["events"].append({
            "type": "mood",
            "value": mood.mood,
            "time": str(mood.created_at)
        })

    for crisis in crises:
        if not crisis.created_at:
            continue

        dateKey = crisis.created_at.strftime("%Y-%m-%d")
        grouped[dateKey]["date"] = dateKey
        grouped[dateKey]["riskLevel"] = crisis.risk_level
        grouped[dateKey]["recoveryStatus"] = crisis.recovery_status

        grouped[dateKey]["events"].append({
            "type": "crisis",
            "riskLevel": crisis.risk_level,
            "recoveryStatus": crisis.recovery_status,
            "time": str(crisis.created_at)
        })

    timeline = sorted(
        grouped.values(),
        key=lambda x: x["date"]
    )

    return timeline[-30:]