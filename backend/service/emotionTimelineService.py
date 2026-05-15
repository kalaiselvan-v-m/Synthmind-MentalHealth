from sqlalchemy.orm import Session
from collections import Counter
from datetime import datetime, timedelta

from backend.models.chat import ChatHistory


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