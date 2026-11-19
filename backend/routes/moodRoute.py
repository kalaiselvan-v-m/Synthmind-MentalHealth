from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.mood import Mood
from backend.models.user import User
from backend.schemas.moodSchema import MoodCreate

router = APIRouter(prefix="/mood", tags=["Mood"])


@router.post("/checkin")
def checkin_mood(
    data: MoodCreate,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    new_mood = Mood(
        user_id=currentUser.id,
        mood=data.mood,
        note=data.note,
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    return {"message": "Mood recorded successfully", "id": new_mood.id}


@router.get("/history")
def get_mood_history(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    return (
        db.query(Mood)
        .filter(Mood.user_id == currentUser.id)
        .order_by(Mood.created_at.desc())
        .all()
    )


@router.get("/summary")
def get_mood_summary(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    moods = db.query(Mood).filter(Mood.user_id == currentUser.id).all()
    if not moods:
        return {
            "total_entries": 0,
            "mood_distribution": {"Happy": 0, "Normal": 0, "Low": 0, "Overwhelmed": 0},
            "dominant_mood": "None",
        }

    mood_count = {"Happy": 0, "Normal": 0, "Low": 0, "Overwhelmed": 0}
    for mood in moods:
        if mood.mood in mood_count:
            mood_count[mood.mood] += 1

    return {
        "total_entries": len(moods),
        "mood_distribution": mood_count,
        "dominant_mood": max(mood_count, key=mood_count.get),
    }


@router.get("/calendar")
def get_mood_calendar(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    moods = (
        db.query(Mood)
        .filter(Mood.user_id == currentUser.id)
        .order_by(Mood.created_at.asc())
        .all()
    )

    if not moods:
        return {
            "days": [],
            "dominantMood": "None",
            "positiveDays": 0,
            "negativeDays": 0,
            "insight": "No data yet. Start tracking your mood daily.",
        }

    daily_map = defaultdict(list)
    for item in moods:
        daily_map[item.created_at.date().isoformat()].append(item.mood)

    mood_count = {"Happy": 0, "Normal": 0, "Low": 0, "Overwhelmed": 0}
    emoji_map = {"Happy": "😊", "Normal": "😐", "Low": "😔", "Overwhelmed": "😵"}
    days = []

    for date, mood_list in daily_map.items():
        mood = max(set(mood_list), key=mood_list.count)
        if mood in mood_count:
            mood_count[mood] += 1
        days.append({"date": date, "mood": mood, "emoji": emoji_map.get(mood, "😐")})

    dominant = max(mood_count, key=mood_count.get)
    positive = mood_count["Happy"]
    negative = mood_count["Low"] + mood_count["Overwhelmed"]

    if negative > positive:
        insight = "You’ve had more low or heavy days recently. Consider taking small breaks."
    elif positive > negative:
        insight = "Your mood has been generally positive. Keep doing what works."
    else:
        insight = "Your mood seems balanced. Stay consistent."

    return {
        "days": days,
        "dominantMood": dominant,
        "positiveDays": positive,
        "negativeDays": negative,
        "insight": insight,
    }
