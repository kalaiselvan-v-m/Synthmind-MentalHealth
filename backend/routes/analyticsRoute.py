from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.dependencies.authDependency import getCurrentUser

from backend.config.database import get_db
from backend.service.analyticsService import getMoodTimeline
from backend.service.emotionTimelineService import buildVisualEmotionTimeline

from backend.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/timeline/{user_id}")
def getTimeline(user_id: int, db: Session = Depends(get_db)):
    return getMoodTimeline(db, user_id)

@router.get("/emotion-timeline")
def emotionTimeline(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return buildVisualEmotionTimeline(db, currentUser.id)