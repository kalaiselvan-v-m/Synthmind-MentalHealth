from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.service.analyticsService import getMoodTimeline

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/timeline/{user_id}")
def getTimeline(user_id: int, db: Session = Depends(get_db)):
    return getMoodTimeline(db, user_id)