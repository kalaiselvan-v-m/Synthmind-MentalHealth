from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from collections import Counter, defaultdict

from backend.models.chat import ChatHistory
from backend.models.journal import JournalEntry
from backend.models.mood import Mood
from backend.models.habit import HabitCompletion
from backend.service.weeklyReportService import generateWeeklyReport


NEGATIVE_EMOTIONS = [
    "fear",
    "sadness",
    "grief",
    "nervousness",
    "remorse",
    "disappointment",
    "anger"
]

POSITIVE_EMOTIONS = [
    "joy",
    "relief",
    "admiration",
    "gratitude",
    "optimism",
    "calm",
    "excitement",
    "curiosity",
    "neutral"
]

LOW_MOODS = [
    "Low",
    "Overwhelmed",
    "low",
    "overwhelmed"
]

GOOD_MOODS = [
    "Happy",
    "Normal",
    "happy",
    "normal"
]


# ------------------------------------------------
# 🔹 RECENT DATA FETCHERS
# ------------------------------------------------
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


def getRecentHabitCompletions(
    db: Session,
    user_id: int,
    days: int = 14
):
    since = datetime.utcnow().date() - timedelta(days=days)

    return (
        db.query(HabitCompletion)
        .filter(HabitCompletion.user_id == user_id)
        .filter(HabitCompletion.completed_date >= since)
        .order_by(HabitCompletion.completed_date.asc())
        .all()
    )


# ------------------------------------------------
# 🔹 EMOTION HELPERS
# ------------------------------------------------
def isNegativeEmotion(emotion: str):
    return emotion in NEGATIVE_EMOTIONS


def isPositiveEmotion(emotion: str):
    return emotion in POSITIVE_EMOTIONS


# ------------------------------------------------
# 🔹 DAILY EMOTIONAL MAP
# ------------------------------------------------
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

    # chats
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

    # journals
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

    # moods
    for mood in moods:
        if not mood.created_at:
            continue

        day = mood.created_at.strftime("%Y-%m-%d")

        daily[day]["moods"].append(mood.mood)

        if mood.mood in LOW_MOODS:
            daily[day]["negativeCount"] += 1

        elif mood.mood in GOOD_MOODS:
            daily[day]["positiveCount"] += 1

    # habits
    for habit in habits:
        day = habit.completed_date.strftime("%Y-%m-%d")
        daily[day]["habits"] += 1

    return daily


# ------------------------------------------------
# 🔹 JOURNAL EFFECT
# ------------------------------------------------
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
        return (
            "You seem a little steadier on days when you journal."
        )

    if avgJournal < avgNonJournal:
        return (
            "Journaling days seem to happen around heavier emotions, "
            "which may mean you use journaling when things feel difficult."
        )

    return None


# ------------------------------------------------
# 🔹 HABIT EFFECT
# ------------------------------------------------
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
        return (
            "Your emotional pattern looks better on days "
            "when you complete a habit."
        )

    if avgHabit < avgNonHabit:
        return (
            "You tend to complete habits on tougher days, "
            "which shows you are using support tools when needed."
        )

    return None


# ------------------------------------------------
# 🔹 RECURRING THEMES
# ------------------------------------------------
def detectRecurringTheme(chats, journals):
    text = " ".join(
        [chat.message.lower() for chat in chats if chat.message] +
        [journal.content.lower() for journal in journals if journal.content]
    )

    themes = []

    if any(word in text for word in [
        "exam",
        "test",
        "assignment",
        "deadline"
    ]):
        themes.append(
            "Academic pressure appears to be one recurring emotional theme."
        )

    if any(word in text for word in [
        "interview",
        "placement",
        "job",
        "career"
    ]):
        themes.append(
            "Career or interview pressure appears to affect your emotional state."
        )

    if any(word in text for word in [
        "sleep",
        "tired",
        "insomnia",
        "awake"
    ]):
        themes.append(
            "Sleep or tiredness may be connected to your emotional changes."
        )

    if any(word in text for word in [
        "alone",
        "lonely",
        "isolated"
    ]):
        themes.append(
            "Feeling alone appears as a recurring emotional signal."
        )

    if any(word in text for word in [
        "overthinking",
        "anxious",
        "anxiety"
    ]):
        themes.append(
            "Overthinking or anxiety appears repeatedly in your recent check-ins."
        )

    return themes[:3]


# ------------------------------------------------
# 🔹 EMOTIONAL PATTERNS
# ------------------------------------------------
def detectEmotionalPatterns(chats):
    insights = []

    lonelyKeywords = [
        "alone",
        "lonely",
        "nobody cares",
        "invisible",
        "worthless",
        "not important",
        "dont feel worthy",
        "don't feel worthy",
    ]

    exhaustionKeywords = [
        "tired",
        "drained",
        "exhausted",
        "burned out",
        "burnt out",
        "overwhelmed",
        "mentally tired",
    ]

    selfCriticalKeywords = [
        "failed",
        "failure",
        "useless",
        "hate myself",
        "not good enough",
        "losing myself",
        "not myself",
    ]

    lonelyCount = 0
    exhaustionCount = 0
    selfCriticalCount = 0

    for chat in chats:
        msg = (chat.message or "").lower()

        if any(word in msg for word in lonelyKeywords):
            lonelyCount += 1

        if any(word in msg for word in exhaustionKeywords):
            exhaustionCount += 1

        if any(word in msg for word in selfCriticalKeywords):
            selfCriticalCount += 1

    if lonelyCount >= 3:
        insights.append({
            "type": "loneliness_pattern",
            "title": "Emotional Disconnection",
            "message": (
                "You’ve mentioned feeling emotionally disconnected "
                "several times recently."
            )
        })

    if exhaustionCount >= 3:
        insights.append({
            "type": "mental_exhaustion",
            "title": "Mental Exhaustion",
            "message": (
                "You’ve seemed mentally exhausted lately."
            )
        })

    if selfCriticalCount >= 2:
        insights.append({
            "type": "self_critical_pattern",
            "title": "Self-Critical Thinking",
            "message": (
                "You’ve been speaking more critically about yourself recently."
            )
        })

    return insights


# ------------------------------------------------
# 🔹 EMOTION SHIFT
# ------------------------------------------------
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

    firstHalf = [
        emotion for _, emotion in items[:midpoint]
    ]

    secondHalf = [
        emotion for _, emotion in items[midpoint:]
    ]

    firstNeg = sum(
        1 for e in firstHalf if isNegativeEmotion(e)
    )

    secondNeg = sum(
        1 for e in secondHalf if isNegativeEmotion(e)
    )

    firstPos = sum(
        1 for e in firstHalf if isPositiveEmotion(e)
    )

    secondPos = sum(
        1 for e in secondHalf if isPositiveEmotion(e)
    )

    if secondNeg < firstNeg and secondPos >= firstPos:
        return (
            "Your recent emotional pattern looks slightly "
            "more stable than earlier."
        )

    if secondNeg > firstNeg:
        return (
            "Your recent entries show a slight increase "
            "in heavier emotions."
        )

    return None

# ------------------------------------------------
# 🔹 EMOTION JOURNEY
# ------------------------------------------------
def buildEmotionJourney(chats):
    timeline = []

    grouped = defaultdict(list)

    for chat in chats:
        if not chat.created_at:
            continue

        day = chat.created_at.strftime("%b %d")

        grouped[day].append(chat)

    for day, items in grouped.items():

        emotions = [
            c.emotion for c in items if c.emotion
        ]

        dominant = "neutral"

        if emotions:
            dominant = Counter(emotions).most_common(1)[0][0]

        messageText = " ".join(
            [
                (c.message or "").lower()
                for c in items
            ]
        )

        summary = "Emotionally balanced day."

        if "lonely" in messageText or "alone" in messageText:
            summary = (
                "Feelings of emotional disconnection appeared."
            )

        elif (
            "tired" in messageText
            or "exhausted" in messageText
            or "drained" in messageText
        ):
            summary = (
                "Mental exhaustion appeared throughout conversations."
            )

        elif dominant in ["joy", "gratitude", "relief"]:
            summary = (
                "Conversations felt emotionally lighter."
            )

        elif dominant in ["sadness", "fear", "grief"]:
            summary = (
                "Emotionally heavier conversations appeared."
            )

        timeline.append({
            "date": day,
            "dominantEmotion": dominant,
            "summary": summary
        })

    return timeline[-7:]
# ------------------------------------------------
# 🔹 MOOD HEATMAP
# ------------------------------------------------
def buildMoodHeatmap(chats, moods):
    grouped = defaultdict(list)

    # chat emotions
    for chat in chats:
        if not chat.created_at:
            continue

        day = chat.created_at.strftime("%Y-%m-%d")

        grouped[day].append(
            chat.emotion or "neutral"
        )

    # mood entries
    for mood in moods:
        if not mood.created_at:
            continue

        day = mood.created_at.strftime("%Y-%m-%d")

        grouped[day].append(
            mood.mood or "Normal"
        )

    heatmap = []

    for day, values in grouped.items():

        negative = 0
        positive = 0

        for value in values:

            lower = value.lower()

            if lower in [
                "fear",
                "sadness",
                "grief",
                "nervousness",
                "anger",
                "low",
                "overwhelmed"
            ]:
                negative += 1

            else:
                positive += 1

        intensity = "neutral"

        if negative >= 4:
            intensity = "heavy"

        elif negative >= 2:
            intensity = "low"

        elif positive >= negative:
            intensity = "positive"

        heatmap.append({
            "date": day,
            "intensity": intensity,
            "negativeCount": negative,
            "positiveCount": positive
        })

    return sorted(
        heatmap,
        key=lambda x: x["date"]
    )[-30:]

def buildWeeklyReflection(report, insights):
    trend = report.get("trend", "Mixed emotional week")
    dominantEmotion = report.get("dominantEmotion", "neutral")
    negativeCount = report.get("negativeCount", 0)
    positiveCount = report.get("positiveCount", 0)

    if negativeCount >= 4:
        message = (
            "This week seems to have carried some heavier moments. "
            "Try keeping your next steps gentle instead of pushing yourself too hard."
        )

    elif positiveCount > negativeCount:
        message = (
            "This week shows some steadier emotional signals. "
            "It looks like there were moments where things felt a little lighter."
        )

    elif dominantEmotion in ["sadness", "fear", "nervousness", "grief"]:
        message = (
            "This week feels emotionally mixed, with some signs of mental weight. "
            "Small calming routines may help you feel more grounded."
        )

    else:
        message = (
            "This week looks emotionally balanced overall. "
            "Keep checking in with yourself so SynthMind can notice deeper patterns."
        )

    return {
        "title": "Weekly Reflection",
        "trend": trend,
        "dominantEmotion": dominantEmotion,
        "message": message
    }
# ------------------------------------------------
# 🔹 BUILD INSIGHTS
# ------------------------------------------------
def buildEmotionalInsights(db: Session, user_id: int):
    report = generateWeeklyReport(db, user_id)

    chats = getRecentChats(db, user_id)
    journals = getRecentJournals(db, user_id)
    moods = getRecentMoods(db, user_id)
    habits = getRecentHabitCompletions(db, user_id)
    
    daily = buildDailyMap(
        chats,
        journals,
        moods,
        habits
    )

    insights = []

    # emotional patterns
    patternInsights = detectEmotionalPatterns(chats)
    insights.extend(patternInsights)

    # emotional shift
    shiftInsight = detectEmotionShift(chats, journals)

    if shiftInsight:
        insights.append({
            "type": "emotional_shift",
            "title": "Emotional Shift",
            "message": shiftInsight
        })

    # journal effect
    journalInsight = detectJournalEffect(daily)

    if journalInsight:
        insights.append({
            "type": "journal_effect",
            "title": "Journal Pattern",
            "message": journalInsight
        })

    # habit effect
    habitInsight = detectHabitEffect(daily)

    if habitInsight:
        insights.append({
            "type": "habit_effect",
            "title": "Habit Pattern",
            "message": habitInsight
        })

    # recurring themes
    for theme in detectRecurringTheme(chats, journals):
        insights.append({
            "type": "recurring_theme",
            "title": "Recurring Theme",
            "message": theme
        })

    # heavy week
    if report.get("negativeCount", 0) >= 4:
        insights.append({
            "type": "heavy_week",
            "title": "Heavy Moments",
            "message": (
                "This week had several emotionally heavy moments, "
                "so gentle routines may help more than big changes."
            )
        })

    # positive trend
    if report.get("positiveCount", 0) > report.get("negativeCount", 0):
        insights.append({
            "type": "positive_trend",
            "title": "Positive Trend",
            "message": (
                "Your recent pattern shows more stable or positive "
                "signals than heavy ones."
            )
        })

    # fallback
    if not insights:
        insights.append({
            "type": "starter",
            "title": "Start Building Patterns",
            "message": (
                "Keep chatting, journaling, and checking in with mood "
                "so SynthMind can notice useful patterns over time."
            )
        })

    return {
        "dominantEmotion": report.get(
            "dominantEmotion",
            "neutral"
        ),

        "trend": report.get(
            "trend",
            "No activity this week"
        ),

        "totalChats": report.get(
            "totalChats",
            0
        ),
        

        "totalJournals": report.get(
            "totalJournals",
            0
        ),

        "emotionJourney": buildEmotionJourney(chats),
        "moodHeatmap": buildMoodHeatmap(chats, moods),
        "weeklyReflection": buildWeeklyReflection(report, insights),
        "insights": insights[:6]
    }