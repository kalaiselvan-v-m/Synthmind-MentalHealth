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
    emotions = [c.emotion for c in chats if c.emotion]

    if not emotions:
        return "neutral"

    return Counter(emotions).most_common(1)[0][0]


# -------------------------------
# 🔹 DETECT NEGATIVE STREAK
# -------------------------------
def detectNegativeStreak(chats):
    streak = 0

    for chat in reversed(chats):
        if chat.emotion in ["fear", "sadness", "grief", "nervousness"]:
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

    negative = 0
    positive = 0

    for c in recent:
        if c.emotion in ["fear", "sadness", "grief"]:
            negative += 1
        if c.emotion in ["joy", "calm", "relief"]:
            positive += 1

    return positive > negative


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

    summary = f"""
Emotional Timeline:
- Dominant emotion: {dominant}
- Negative streak: {streak}
- Improving: {improving}
"""

    return summary