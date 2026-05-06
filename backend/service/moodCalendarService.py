from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from backend.models.chat import ChatHistory
from backend.models.journal import JournalEntry


NEGATIVE_EMOTIONS = [
    "fear", "sadness", "grief", "nervousness",
    "remorse", "disappointment", "anger"
]

POSITIVE_EMOTIONS = [
    "joy", "relief", "admiration", "gratitude",
    "optimism", "calm", "excitement", "curiosity"
]


def classifyEmotion(emotion: str):
    if emotion in NEGATIVE_EMOTIONS:
        return "negative"
    if emotion in POSITIVE_EMOTIONS:
        return "positive"
    return "neutral"


def buildMoodCalendar(db: Session, user_id: int, days: int = 30):
    since = datetime.utcnow() - timedelta(days=days)

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .filter(ChatHistory.created_at >= since)
        .all()
    )

    journals = (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .filter(JournalEntry.created_at >= since)
        .all()
    )

    daily = defaultdict(lambda: {
        "date": "",
        "total": 0,
        "chatCount": 0,
        "journalCount": 0,
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "emotions": []
    })

    for chat in chats:
        day = chat.created_at.strftime("%Y-%m-%d")
        emotion = chat.emotion or "neutral"
        emotionType = classifyEmotion(emotion)

        daily[day]["date"] = day
        daily[day]["total"] += 1
        daily[day]["chatCount"] += 1
        daily[day][emotionType] += 1
        daily[day]["emotions"].append(emotion)

    for journal in journals:
        day = journal.created_at.strftime("%Y-%m-%d")
        emotion = journal.emotion or "neutral"
        emotionType = classifyEmotion(emotion)

        daily[day]["date"] = day
        daily[day]["total"] += 1
        daily[day]["journalCount"] += 1
        daily[day][emotionType] += 1
        daily[day]["emotions"].append(emotion)

    result = []

    for i in range(days - 1, -1, -1):
        date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")

        item = daily[date]
        item["date"] = date

        if item["emotions"]:
            item["dominantEmotion"] = Counter(item["emotions"]).most_common(1)[0][0]
        else:
            item["dominantEmotion"] = "none"

        if item["total"] == 0:
            item["moodType"] = "empty"
        elif item["negative"] > item["positive"]:
            item["moodType"] = "negative"
        elif item["positive"] > item["negative"]:
            item["moodType"] = "positive"
        else:
            item["moodType"] = "neutral"

        result.append(item)

    return result