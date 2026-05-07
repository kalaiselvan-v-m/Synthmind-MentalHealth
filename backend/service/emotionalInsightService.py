from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import Counter, defaultdict

from backend.models.chat import ChatHistory
from backend.models.journal import JournalEntry
from backend.models.mood import Mood
from backend.models.habit import HabitCompletion
from backend.service.weeklyReportService import generateWeeklyReport


NEGATIVE_EMOTIONS = [
    "fear", "sadness", "grief", "nervousness",
    "remorse", "disappointment", "anger"
]

POSITIVE_EMOTIONS = [
    "joy", "relief", "admiration", "gratitude",
    "optimism", "calm", "excitement", "curiosity", "neutral"
]

LOW_MOODS = ["Low", "Overwhelmed", "low", "overwhelmed"]
GOOD_MOODS = ["Happy", "Normal", "happy", "normal"]


def getRecentChats(db: Session, user_id: int, days: int = 14):
    since = datetime.utcnow() - timedelta(days=days)

    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .filter(ChatHistory.created_at >= since)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )


def getRecentJournals(db: Session, user_id: int, days: int = 14):
    since = datetime.utcnow() - timedelta(days=days)

    return (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .filter(JournalEntry.created_at >= since)
        .order_by(JournalEntry.created_at.asc())
        .all()
    )


def getRecentMoods(db: Session, user_id: int, days: int = 14):
    since = datetime.utcnow() - timedelta(days=days)

    return (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .filter(Mood.created_at >= since)
        .order_by(Mood.created_at.asc())
        .all()
    )


def getRecentHabitCompletions(db: Session, user_id: int, days: int = 14):
    since = datetime.utcnow().date() - timedelta(days=days)

    return (
        db.query(HabitCompletion)
        .filter(HabitCompletion.user_id == user_id)
        .filter(HabitCompletion.completed_date >= since)
        .order_by(HabitCompletion.completed_date.asc())
        .all()
    )


def isNegativeEmotion(emotion: str):
    return emotion in NEGATIVE_EMOTIONS


def isPositiveEmotion(emotion: str):
    return emotion in POSITIVE_EMOTIONS


def buildDailyMap(chats, journals, moods, habits):
    daily = defaultdict(lambda: {
        "chatEmotions": [],
        "journalEmotions": [],
        "moods": [],
        "habits": 0,
        "journalCount": 0,
        "negativeCount": 0,
        "positiveCount": 0
    })

    for chat in chats:
        if not chat.created_at:
            continue

        day = chat.created_at.strftime("%Y-%m-%d")
        emotion = chat.emotion or "neutral"

        daily[day]["chatEmotions"].append(emotion)

        if isNegativeEmotion(emotion):
            daily[day]["negativeCount"] += 1
        elif isPositiveEmotion(emotion):
            daily[day]["positiveCount"] += 1

    for journal in journals:
        if not journal.created_at:
            continue

        day = journal.created_at.strftime("%Y-%m-%d")
        emotion = journal.emotion or "neutral"

        daily[day]["journalEmotions"].append(emotion)
        daily[day]["journalCount"] += 1

        if isNegativeEmotion(emotion):
            daily[day]["negativeCount"] += 1
        elif isPositiveEmotion(emotion):
            daily[day]["positiveCount"] += 1

    for mood in moods:
        if not mood.created_at:
            continue

        day = mood.created_at.strftime("%Y-%m-%d")
        daily[day]["moods"].append(mood.mood)

        if mood.mood in LOW_MOODS:
            daily[day]["negativeCount"] += 1
        elif mood.mood in GOOD_MOODS:
            daily[day]["positiveCount"] += 1

    for habit in habits:
        day = habit.completed_date.strftime("%Y-%m-%d")
        daily[day]["habits"] += 1

    return daily


def detectJournalEffect(daily):
    journalDays = []
    nonJournalDays = []

    for _, values in daily.items():
        score = values["positiveCount"] - values["negativeCount"]

        if values["journalCount"] > 0:
            journalDays.append(score)
        else:
            nonJournalDays.append(score)

    if len(journalDays) < 1 or len(nonJournalDays) < 1:
        return None

    avgJournal = sum(journalDays) / len(journalDays)
    avgNonJournal = sum(nonJournalDays) / len(nonJournalDays)

    if avgJournal > avgNonJournal:
        return "You seem a little steadier on days when you journal."

    if avgJournal < avgNonJournal:
        return "Journaling days seem to happen around heavier emotions, which may mean you use journaling when things feel difficult."

    return None


def detectHabitEffect(daily):
    habitDays = []
    nonHabitDays = []

    for _, values in daily.items():
        score = values["positiveCount"] - values["negativeCount"]

        if values["habits"] > 0:
            habitDays.append(score)
        else:
            nonHabitDays.append(score)

    if len(habitDays) < 1 or len(nonHabitDays) < 1:
        return None

    avgHabit = sum(habitDays) / len(habitDays)
    avgNonHabit = sum(nonHabitDays) / len(nonHabitDays)

    if avgHabit > avgNonHabit:
        return "Your emotional pattern looks better on days when you complete a habit."

    if avgHabit < avgNonHabit:
        return "You tend to complete habits on tougher days, which shows you are using support tools when needed."

    return None


def detectRecurringTheme(chats, journals):
    text = " ".join(
        [chat.message.lower() for chat in chats if chat.message] +
        [journal.content.lower() for journal in journals if journal.content]
    )

    themes = []

    if any(word in text for word in ["exam", "test", "assignment", "deadline"]):
        themes.append("Academic pressure appears to be one recurring emotional theme.")

    if any(word in text for word in ["interview", "placement", "job", "career"]):
        themes.append("Career or interview pressure appears to affect your emotional state.")

    if any(word in text for word in ["sleep", "tired", "insomnia", "awake"]):
        themes.append("Sleep or tiredness may be connected to your emotional changes.")

    if any(word in text for word in ["alone", "lonely", "isolated"]):
        themes.append("Feeling alone appears as a recurring emotional signal.")

    if any(word in text for word in ["overthinking", "anxious", "anxiety"]):
        themes.append("Overthinking or anxiety appears repeatedly in your recent check-ins.")

    return themes[:2]


def detectEmotionShift(chats, journals):
    items = []

    for chat in chats:
        if chat.emotion and chat.created_at:
            items.append((chat.created_at, chat.emotion))

    for journal in journals:
        if journal.emotion and journal.created_at:
            items.append((journal.created_at, journal.emotion))

    items = sorted(items, key=lambda x: x[0])

    if len(items) < 4:
        return None

    midpoint = len(items) // 2
    firstHalf = [emotion for _, emotion in items[:midpoint]]
    secondHalf = [emotion for _, emotion in items[midpoint:]]

    firstNeg = sum(1 for e in firstHalf if isNegativeEmotion(e))
    secondNeg = sum(1 for e in secondHalf if isNegativeEmotion(e))

    firstPos = sum(1 for e in firstHalf if isPositiveEmotion(e))
    secondPos = sum(1 for e in secondHalf if isPositiveEmotion(e))

    if secondNeg < firstNeg and secondPos >= firstPos:
        return "Your recent emotional pattern looks slightly more stable than earlier."

    if secondNeg > firstNeg:
        return "Your recent entries show a slight increase in heavier emotions."

    return None


def buildEmotionalInsights(db: Session, user_id: int):
    report = generateWeeklyReport(db, user_id)

    chats = getRecentChats(db, user_id)
    journals = getRecentJournals(db, user_id)
    moods = getRecentMoods(db, user_id)
    habits = getRecentHabitCompletions(db, user_id)

    daily = buildDailyMap(chats, journals, moods, habits)

    insights = []

    shiftInsight = detectEmotionShift(chats, journals)
    if shiftInsight:
        insights.append({
            "type": "emotional_shift",
            "title": "Emotional Shift",
            "message": shiftInsight
        })

    journalInsight = detectJournalEffect(daily)
    if journalInsight:
        insights.append({
            "type": "journal_effect",
            "title": "Journal Pattern",
            "message": journalInsight
        })

    habitInsight = detectHabitEffect(daily)
    if habitInsight:
        insights.append({
            "type": "habit_effect",
            "title": "Habit Pattern",
            "message": habitInsight
        })

    for theme in detectRecurringTheme(chats, journals):
        insights.append({
            "type": "recurring_theme",
            "title": "Recurring Theme",
            "message": theme
        })

    if report.get("negativeCount", 0) >= 4:
        insights.append({
            "type": "heavy_week",
            "title": "Heavy Moments",
            "message": "This week had several emotionally heavy moments, so gentle routines may help more than big changes."
        })

    if report.get("positiveCount", 0) > report.get("negativeCount", 0):
        insights.append({
            "type": "positive_trend",
            "title": "Positive Trend",
            "message": "Your recent pattern shows more stable or positive signals than heavy ones."
        })

    if not insights:
        insights.append({
            "type": "starter",
            "title": "Start Building Patterns",
            "message": "Keep chatting, journaling, and checking in with mood so SynthMind can notice useful patterns over time."
        })

    return {
        "dominantEmotion": report.get("dominantEmotion", "neutral"),
        "trend": report.get("trend", "No activity this week"),
        "totalChats": report.get("totalChats", 0),
        "totalJournals": report.get("totalJournals", 0),
        "insights": insights[:5]
    }