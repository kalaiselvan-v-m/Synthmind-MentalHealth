from sqlalchemy.orm import Session
from collections import defaultdict, Counter

from backend.models.mood import Mood
from backend.models.chat import ChatHistory
from backend.service.riskService import calculateRiskScore


riskValueMap = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

moodValueMap = {
    "Happy": 4,
    "Normal": 3,
    "Low": 2,
    "Overwhelmed": 1,
    "Unknown": 0
}

negativeEmotions = [
    "sadness", "grief", "fear", "nervousness",
    "remorse", "disappointment", "anger"
]


def getMoodTimeline(db: Session, user_id: int):
    timeline = []

    moods = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.created_at.asc())
        .all()
    )

    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.asc())
        .all()
    )

    mood_by_date = {}
    emotion_by_date = defaultdict(list)

    for mood in moods:
        date = mood.created_at.date()
        mood_by_date[date] = mood.mood

    for chat in chats:
        date = chat.created_at.date()
        if chat.emotion:
            emotion_by_date[date].append(chat.emotion)

    all_dates = sorted(set(list(mood_by_date.keys()) + list(emotion_by_date.keys())))

    currentRisk = calculateRiskScore(db, user_id)["final_risk"]

    for date in all_dates:
        emotions = emotion_by_date.get(date, [])

        topEmotion = "neutral"
        if emotions:
            topEmotion = Counter(emotions).most_common(1)[0][0]

        timeline.append({
            "date": str(date),
            "mood": mood_by_date.get(date, "Unknown"),
            "emotion": topEmotion,
            "risk": currentRisk
        })

    trend = analyzeTrend(timeline)

    return {
        "user_id": user_id,
        "timeline": timeline,
        "trend_analysis": trend
    }


def analyzeTrend(timeline: list):
    if not timeline:
        return {
            "overall_trend": "No data",
            "mood_trend": "No data",
            "risk_trend": "No data",
            "dominant_emotion": "Unknown",
            "negative_emotion_count": 0,
            "insight": "No timeline data available yet."
        }

    moods = [item["mood"] for item in timeline]
    emotions = [item["emotion"] for item in timeline]
    risks = [item["risk"] for item in timeline]

    moodScores = [moodValueMap.get(mood, 0) for mood in moods]
    riskScores = [riskValueMap.get(risk, 1) for risk in risks]

    firstMood = moodScores[0]
    lastMood = moodScores[-1]

    firstRisk = riskScores[0]
    lastRisk = riskScores[-1]

    negativeCount = sum(1 for emotion in emotions if emotion in negativeEmotions)

    dominantEmotion = Counter(emotions).most_common(1)[0][0]

    if lastMood > firstMood:
        moodTrend = "Improving"
    elif lastMood < firstMood:
        moodTrend = "Declining"
    else:
        moodTrend = "Stable"

    if lastRisk > firstRisk:
        riskTrend = "Increasing"
    elif lastRisk < firstRisk:
        riskTrend = "Decreasing"
    else:
        riskTrend = "Stable"

    if moodTrend == "Improving" and riskTrend != "Increasing":
        overallTrend = "Positive"
        insight = "Your emotional pattern shows signs of improvement."
    elif moodTrend == "Declining" or riskTrend == "Increasing":
        overallTrend = "Needs Attention"
        insight = "Your recent pattern may need more care and support."
    else:
        overallTrend = "Stable"
        insight = "Your emotional state appears mostly stable."

    return {
        "overall_trend": overallTrend,
        "mood_trend": moodTrend,
        "risk_trend": riskTrend,
        "dominant_emotion": dominantEmotion,
        "negative_emotion_count": negativeCount,
        "insight": insight
    }