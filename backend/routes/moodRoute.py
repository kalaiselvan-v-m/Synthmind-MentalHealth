from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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