from sqlalchemy.orm import Session

from backend.service.riskService import calculateRiskScore
from backend.service.analyticsService import getMoodTimeline
from backend.service.recommendationService import getPersonalizedRecommendations


def buildRecoveryPlan(db: Session, user_id: int):
    riskData = calculateRiskScore(db, user_id)
    riskLevel = riskData["final_risk"]

    timelineData = getMoodTimeline(db, user_id)
    trend = timelineData.get("trend_analysis", {})

    recommendationData = getPersonalizedRecommendations(db, user_id)
    recommendations = recommendationData.get("recommendations", [])

    if riskLevel == "High":
        dailyRoutine = [
            "Do a morning mood check-in.",
            "Practice 5 minutes of slow breathing.",
            "Send a message or call one trusted person.",
            "Avoid staying isolated for long periods."
        ]
        therapySuggestion = "Professional support is strongly recommended if distress continues."
    elif riskLevel == "Medium":
        dailyRoutine = [
            "Do a morning mood check-in.",
            "Complete one CBT reflection.",
            "Take a 10-minute walk or stretch break.",
            "Write one thing that felt manageable today."
        ]
        therapySuggestion = "Consider speaking with a counselor or trusted person if stress continues."
    else:
        dailyRoutine = [
            "Do a daily mood check-in.",
            "Write one positive or neutral thought.",
            "Take one mindful pause during the day.",
            "Maintain a healthy sleep routine."
        ]
        therapySuggestion = "Continue regular self-care and monitoring."

    plan = {
        "user_id": user_id,
        "risk_level": riskLevel,
        "overall_trend": trend.get("overall_trend", "Unknown"),
        "dominant_emotion": trend.get("dominant_emotion", "Unknown"),
        "daily_routine": dailyRoutine,
        "breathing_exercise": "Try 4-7-8 breathing: inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds.",
        "journaling_task": "Write: What am I feeling? What triggered it? What do I need right now?",
        "cbt_task": "Write one negative thought and replace it with one kinder, realistic thought.",
        "sleep_tip": "Avoid screens 30 minutes before sleep and keep a regular sleep time.",
        "habit_goal": "Complete one small self-care action today.",
        "recommended_activities": recommendations[:5],
        "therapy_suggestion": therapySuggestion,
        "note": "This is an AI-generated wellness care plan, not a medical diagnosis or treatment plan."
    }

    return plan