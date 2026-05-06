from sqlalchemy.orm import Session

from backend.service.weeklyReportService import generateWeeklyReport
from backend.models.onboarding import UserMentalProfile


def buildHabitSuggestions(db: Session, user_id: int):
    report = generateWeeklyReport(db, user_id)

    profile = (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )

    dominantEmotion = report.get("dominantEmotion", "neutral")
    negativeCount = report.get("negativeCount", 0)
    positiveCount = report.get("positiveCount", 0)
    totalJournals = report.get("totalJournals", 0)
    trend = report.get("trend", "Mixed emotional week")

    habits = []

    if dominantEmotion in ["nervousness", "fear", "anxiety"]:
        habits.append({
            "title": "2-Minute Breathing Reset",
            "category": "Calm",
            "reason": "Your recent pattern shows nervous or fear-based emotions.",
            "steps": [
                "Inhale slowly for 4 seconds",
                "Hold for 2 seconds",
                "Exhale for 6 seconds",
                "Repeat 3 times"
            ],
            "frequency": "Whenever stress feels high",
            "difficulty": "Easy"
        })

    if dominantEmotion in ["sadness", "grief", "disappointment"]:
        habits.append({
            "title": "One Small Win",
            "category": "Mood Support",
            "reason": "Low mood patterns can improve with small achievable actions.",
            "steps": [
                "Choose one tiny task",
                "Complete it without pressure",
                "Write down what you finished"
            ],
            "frequency": "Once daily",
            "difficulty": "Easy"
        })

    if negativeCount >= 3:
        habits.append({
            "title": "Grounding Check",
            "category": "Emotional Regulation",
            "reason": "You had repeated heavy emotions this week.",
            "steps": [
                "Name 3 things you can see",
                "Name 2 things you can feel",
                "Name 1 thing you can hear",
                "Relax your shoulders"
            ],
            "frequency": "During emotional spikes",
            "difficulty": "Easy"
        })

    if totalJournals == 0:
        habits.append({
            "title": "Short Journal Note",
            "category": "Reflection",
            "reason": "You have not journaled this week yet.",
            "steps": [
                "Write 2 lines about your day",
                "Mention one emotion",
                "Mention one thing that helped"
            ],
            "frequency": "3 times a week",
            "difficulty": "Easy"
        })

    if totalJournals >= 1:
        habits.append({
            "title": "Weekly Reflection Review",
            "category": "Self-awareness",
            "reason": "Your journal entries can help identify emotional patterns.",
            "steps": [
                "Read your latest journal insight",
                "Notice the repeated emotion",
                "Pick one helpful action for tomorrow"
            ],
            "frequency": "Once weekly",
            "difficulty": "Medium"
        })

    if profile and profile.stress_score and profile.stress_score >= 70:
        habits.append({
            "title": "Stress Buffer Routine",
            "category": "Stress",
            "reason": "Your profile indicates higher stress levels.",
            "steps": [
                "Take a 5-minute break before intense work",
                "Drink water",
                "Write the next one task only",
                "Start with the easiest part"
            ],
            "frequency": "Before study/work sessions",
            "difficulty": "Easy"
        })

    if profile and profile.support_level and "low" in profile.support_level.lower():
        habits.append({
            "title": "Support Connection",
            "category": "Social Support",
            "reason": "Your profile suggests support may be limited.",
            "steps": [
                "Message one trusted person",
                "Keep it simple",
                "Share only what feels comfortable"
            ],
            "frequency": "Once a week",
            "difficulty": "Medium"
        })

    if positiveCount > negativeCount:
        habits.append({
            "title": "Repeat What Worked",
            "category": "Positive Reinforcement",
            "reason": "Your week shows more positive or stable signals.",
            "steps": [
                "Think of one thing that helped this week",
                "Repeat it tomorrow",
                "Keep it small and realistic"
            ],
            "frequency": "Daily",
            "difficulty": "Easy"
        })

    if not habits:
        habits.append({
            "title": "Daily Check-in",
            "category": "General Wellness",
            "reason": "A simple check-in helps build emotional awareness.",
            "steps": [
                "Pause for 1 minute",
                "Name your current emotion",
                "Choose one small helpful action"
            ],
            "frequency": "Daily",
            "difficulty": "Easy"
        })

    return {
        "trend": trend,
        "dominantEmotion": dominantEmotion,
        "negativeCount": negativeCount,
        "positiveCount": positiveCount,
        "habits": habits[:5]
    }