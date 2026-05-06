from sqlalchemy.orm import Session
from backend.service.weeklyReportService import generateWeeklyReport


def generateSmartReminder(db: Session, user_id: int):
    report = generateWeeklyReport(db, user_id)

    dominant = report.get("dominantEmotion", "neutral")
    negative = report.get("negativeCount", 0)
    positive = report.get("positiveCount", 0)
    totalJournals = report.get("totalJournals", 0)
    totalEntries = report.get("totalEntries", 0)
    trend = report.get("trend", "")

    # No activity yet
    if totalEntries == 0:
        return "Hey, start with one tiny check-in today. Just one line is enough."

    # Emotion-based reminder
    if dominant in ["nervousness", "fear"]:
        return "Hey… things looked a bit tense recently. Just 2 minutes of calm today might help."

    if dominant in ["sadness", "grief", "disappointment"]:
        return "Today doesn’t need to be perfect. One gentle step is enough."

    if dominant in ["anger", "frustration"]:
        return "Take a short pause before pushing through today. A reset might help."

    # Heavy week
    if negative >= 4:
        return "Looks like this week had some heavy moments. Be gentle with yourself today."

    # Journal nudge
    if totalJournals == 0:
        return "A short journal note today could help you understand your mood better."

    # Positive reinforcement
    if positive > negative:
        return "You’ve been doing better lately. Keep that going with one small habit today."

    # Trend-based fallback
    if "improving" in trend.lower():
        return "You’re building a better rhythm. One small habit today can keep it going."

    # Default
    return "Just a small check-in today. You don’t need to do much."