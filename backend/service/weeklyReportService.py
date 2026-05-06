from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import Counter, defaultdict

from backend.models.chat import ChatHistory
from backend.models.journal import JournalEntry
from backend.models.onboarding import UserMentalProfile


NEGATIVE_EMOTIONS = [
    "fear", "sadness", "grief", "nervousness",
    "remorse", "disappointment", "anger"
]

POSITIVE_EMOTIONS = [
    "joy", "relief", "admiration", "gratitude",
    "optimism", "calm", "neutral", "excitement", "curiosity"
]


def getWeeklyChats(db: Session, user_id: int):
    since = datetime.utcnow() - timedelta(days=7)

    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .filter(ChatHistory.created_at >= since)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )


def getWeeklyJournals(db: Session, user_id: int):
    since = datetime.utcnow() - timedelta(days=7)

    return (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .filter(JournalEntry.created_at >= since)
        .order_by(JournalEntry.created_at.asc())
        .all()
    )


def classifyEmotion(emotion: str):
    if emotion in NEGATIVE_EMOTIONS:
        return "negative"

    if emotion in POSITIVE_EMOTIONS:
        return "positive"

    return "neutral"


def getDailyEmotionCounts(chats, journals):
    daily = defaultdict(lambda: {
        "total": 0,
        "chat": 0,
        "journal": 0,
        "positive": 0,
        "negative": 0,
        "neutral": 0
    })

    for chat in chats:
        day = chat.created_at.strftime("%Y-%m-%d") if chat.created_at else "unknown"
        emotionType = classifyEmotion(chat.emotion or "neutral")

        daily[day]["total"] += 1
        daily[day]["chat"] += 1
        daily[day][emotionType] += 1

    for journal in journals:
        day = journal.created_at.strftime("%Y-%m-%d") if journal.created_at else "unknown"
        emotionType = classifyEmotion(journal.emotion or "neutral")

        daily[day]["total"] += 1
        daily[day]["journal"] += 1
        daily[day][emotionType] += 1

    return [
        {
            "date": day,
            "total": values["total"],
            "chat": values["chat"],
            "journal": values["journal"],
            "positive": values["positive"],
            "negative": values["negative"],
            "neutral": values["neutral"]
        }
        for day, values in sorted(daily.items())
    ]


def generateWeeklyReport(db: Session, user_id: int):
    chats = getWeeklyChats(db, user_id)
    journals = getWeeklyJournals(db, user_id)

    profile = (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )

    chatEmotions = [chat.emotion for chat in chats if chat.emotion]
    journalEmotions = [journal.emotion for journal in journals if journal.emotion]

    allEmotions = chatEmotions + journalEmotions
    emotionCounter = Counter(allEmotions)

    totalChats = len(chats)
    totalJournals = len(journals)
    totalEntries = totalChats + totalJournals

    dominantEmotion = (
        emotionCounter.most_common(1)[0][0]
        if allEmotions
        else "neutral"
    )

    negativeCount = sum(1 for e in allEmotions if e in NEGATIVE_EMOTIONS)
    positiveCount = sum(1 for e in allEmotions if e in POSITIVE_EMOTIONS)

    if totalEntries == 0:
        trend = "No activity this week"
        summary = (
            "No weekly emotional pattern is available yet. "
            "Start chatting or journaling to build your weekly report."
        )

    elif negativeCount > positiveCount:
        trend = "Emotionally heavy week"
        summary = (
            "This week shows more emotionally difficult signals across chats and journal entries. "
            "Keep your routine simple and use small grounding habits when things feel intense."
        )

    elif positiveCount > negativeCount:
        trend = "Improving emotional pattern"
        summary = (
            "This week shows more stable or positive emotional signals across your chats and journal entries. "
            "Keep following the habits or situations that helped you feel better."
        )

    else:
        trend = "Mixed emotional week"
        summary = (
            "This week had a mix of emotions. Your chats and journals show both difficult and stable moments. "
            "Notice what triggered emotional changes and what helped you recover."
        )

    recommendations = []

    if negativeCount >= 3:
        recommendations.append("Use short grounding exercises when emotions feel intense.")
        recommendations.append("Talk to someone you trust if the same feeling keeps repeating.")

    if dominantEmotion in ["fear", "nervousness"]:
        recommendations.append("Try slow breathing and reduce pressure before stressful tasks.")

    if dominantEmotion in ["sadness", "grief"]:
        recommendations.append("Keep daily goals small and focus on one gentle activity.")

    if totalJournals == 0:
        recommendations.append("Try writing one short journal entry this week to understand your patterns better.")

    if totalJournals >= 3:
        recommendations.append("You journaled multiple times this week. Review what helped you feel calmer.")

    if profile and profile.support_level and "low" in profile.support_level.lower():
        recommendations.append(
            "Because support level appears low, consider building one small trusted support connection."
        )

    if not recommendations:
        recommendations.append("Continue tracking your mood and checking in regularly.")

    recentJournalInsights = [
        {
            "content": journal.content,
            "emotion": journal.emotion,
            "ai_summary": journal.ai_summary,
            "created_at": journal.created_at
        }
        for journal in journals[-3:]
    ]

    return {
        "totalChats": totalChats,
        "totalJournals": totalJournals,
        "totalEntries": totalEntries,
        "dominantEmotion": dominantEmotion,
        "negativeCount": negativeCount,
        "positiveCount": positiveCount,
        "trend": trend,
        "summary": summary,
        "dailyEmotionCounts": getDailyEmotionCounts(chats, journals),
        "emotionBreakdown": dict(emotionCounter),
        "journalInsights": recentJournalInsights,
        "recommendations": recommendations
    }