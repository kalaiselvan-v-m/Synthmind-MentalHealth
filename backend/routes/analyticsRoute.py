from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.analyticsService import getMoodTimeline
from backend.service.emotionTimelineService import buildVisualEmotionTimeline

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/timeline")
def getTimeline(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    return getMoodTimeline(db, currentUser.id)


@router.get("/emotion-timeline")
def emotionTimeline(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    return buildVisualEmotionTimeline(db, currentUser.id)
