from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from backend.config.database import get_db
from backend.models.mood import Mood
from backend.schemas.moodSchema import MoodCreate

router = APIRouter(prefix="/mood", tags=["Mood"])


# ✅ 1. Check-in mood
@router.post("/checkin")
def checkin_mood(data: MoodCreate, db: Session = Depends(get_db)):
    new_mood = Mood(
        user_id=data.user_id,
        mood=data.mood,
        note=data.note
    )

    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)

    return {"message": "Mood recorded successfully"}


# ✅ 2. Get mood history
@router.get("/history/{user_id}")
def get_mood_history(user_id: int, db: Session = Depends(get_db)):
    moods = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.created_at.desc())
        .all()
    )

    return moods


# ✅ 3. Mood summary (basic analytics)
@router.get("/summary/{user_id}")
def get_mood_summary(user_id: int, db: Session = Depends(get_db)):
    moods = db.query(Mood).filter(Mood.user_id == user_id).all()

    if not moods:
        raise HTTPException(status_code=404, detail="No mood data found")

    mood_count = {
        "Happy": 0,
        "Normal": 0,
        "Low": 0,
        "Overwhelmed": 0
    }

    for m in moods:
        if m.mood in mood_count:
            mood_count[m.mood] += 1

    total = len(moods)

    return {
        "total_entries": total,
        "mood_distribution": mood_count,
        "dominant_mood": max(mood_count, key=mood_count.get)
    }


# ✅ 4. Mood calendar + insights (NEW)
@router.get("/calendar/{user_id}")
def get_mood_calendar(user_id: int, db: Session = Depends(get_db)):
    moods = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.created_at.asc())
        .all()
    )

    if not moods:
        return {
            "days": [],
            "dominantMood": "None",
            "positiveDays": 0,
            "negativeDays": 0,
            "insight": "No data yet. Start tracking your mood daily."
        }

    daily_map = defaultdict(list)

    for m in moods:
        date_str = m.created_at.date().isoformat()
        daily_map[date_str].append(m.mood)

    days = []

    mood_count = {
        "Happy": 0,
        "Normal": 0,
        "Low": 0,
        "Overwhelmed": 0
    }

    emoji_map = {
        "Happy": "😊",
        "Normal": "😐",
        "Low": "😔",
        "Overwhelmed": "😵"
    }

    for date, mood_list in daily_map.items():
        # take most frequent mood of the day
        mood = max(set(mood_list), key=mood_list.count)

        if mood in mood_count:
            mood_count[mood] += 1

        days.append({
            "date": date,
            "mood": mood,
            "emoji": emoji_map.get(mood, "😐")
        })

    dominant = max(mood_count, key=mood_count.get)

    positive = mood_count["Happy"]
    negative = mood_count["Low"] + mood_count["Overwhelmed"]

    # simple insight logic
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
        "insight": insight
    }