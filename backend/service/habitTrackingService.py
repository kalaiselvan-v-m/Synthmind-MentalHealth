from sqlalchemy.orm import Session
from datetime import date, timedelta

from backend.models.habit import HabitCompletion
from backend.service.habitSuggestionService import buildHabitSuggestions


def getRewardInfo(streak: int):
    if streak >= 14:
        return {
            "level": "Legend",
            "badge": "🏆 14-Day Champion",
            "message": "Amazing consistency. This habit is becoming part of your routine.",
            "progress": 100
        }

    if streak >= 7:
        return {
            "level": "Strong",
            "badge": "🔥 7-Day Streak",
            "message": "Great work. You are building real momentum.",
            "progress": 75
        }

    if streak >= 3:
        return {
            "level": "Growing",
            "badge": "🌱 3-Day Builder",
            "message": "Nice progress. Keep the rhythm going.",
            "progress": 45
        }

    if streak >= 1:
        return {
            "level": "Started",
            "badge": "✨ First Step",
            "message": "Good start. One small step still counts.",
            "progress": 20
        }

    return {
        "level": "Not started",
        "badge": "○ Not Started",
        "message": "Start today with one small action.",
        "progress": 0
    }


def markHabitDone(db: Session, user_id: int, habit_title: str, habit_category: str = ""):
    today = date.today()

    existing = (
        db.query(HabitCompletion)
        .filter(
            HabitCompletion.user_id == user_id,
            HabitCompletion.habit_title == habit_title,
            HabitCompletion.completed_date == today
        )
        .first()
    )

    if existing:
        return {
            "message": "Habit already completed today",
            "completed": True
        }

    completion = HabitCompletion(
        user_id=user_id,
        habit_title=habit_title,
        habit_category=habit_category,
        completed_date=today
    )

    db.add(completion)
    db.commit()
    db.refresh(completion)

    return {
        "message": "Habit marked as done",
        "completed": True
    }


def calculateStreak(db: Session, user_id: int, habit_title: str):
    completions = (
        db.query(HabitCompletion)
        .filter(
            HabitCompletion.user_id == user_id,
            HabitCompletion.habit_title == habit_title
        )
        .order_by(HabitCompletion.completed_date.desc())
        .all()
    )

    if not completions:
        return 0

    completed_dates = {item.completed_date for item in completions}

    streak = 0
    current_day = date.today()

    while current_day in completed_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def isCompletedToday(db: Session, user_id: int, habit_title: str):
    today = date.today()

    return (
        db.query(HabitCompletion)
        .filter(
            HabitCompletion.user_id == user_id,
            HabitCompletion.habit_title == habit_title,
            HabitCompletion.completed_date == today
        )
        .first()
        is not None
    )


def getHabitProgress(db: Session, user_id: int):
    suggestions = buildHabitSuggestions(db, user_id)
    habits = suggestions["habits"]

    enriched = []

    for habit in habits:
        title = habit["title"]
        streak = calculateStreak(db, user_id, title)
        reward = getRewardInfo(streak)

        enriched.append({
            **habit,
            "completedToday": isCompletedToday(db, user_id, title),
            "streak": streak,
            "reward": reward
        })

    totalCompletedToday = sum(1 for habit in enriched if habit["completedToday"])
    bestStreak = max([habit["streak"] for habit in enriched], default=0)

    return {
        "trend": suggestions["trend"],
        "dominantEmotion": suggestions["dominantEmotion"],
        "negativeCount": suggestions["negativeCount"],
        "positiveCount": suggestions["positiveCount"],
        "totalCompletedToday": totalCompletedToday,
        "bestStreak": bestStreak,
        "habits": enriched
    }


def getCompletionHistory(db: Session, user_id: int):
    return (
        db.query(HabitCompletion)
        .filter(HabitCompletion.user_id == user_id)
        .order_by(HabitCompletion.completed_date.desc())
        .all()
    )