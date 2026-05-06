from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.moodCalendarService import buildMoodCalendar

router = APIRouter(prefix="/mood-calendar", tags=["Mood Calendar"])


@router.get("")
def getMoodCalendar(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return buildMoodCalendar(db, currentUser.id, days=30)