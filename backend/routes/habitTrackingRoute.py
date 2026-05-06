from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.schemas.habitSchema import HabitCompleteRequest
from backend.service.habitTrackingService import (
    markHabitDone,
    getHabitProgress,
    getCompletionHistory
)

router = APIRouter(prefix="/habit-tracking", tags=["Habit Tracking"])


@router.get("")
def getProgress(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return getHabitProgress(db, currentUser.id)


@router.post("/complete")
def completeHabit(
    data: HabitCompleteRequest,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return markHabitDone(
        db=db,
        user_id=currentUser.id,
        habit_title=data.habit_title,
        habit_category=data.habit_category
    )


@router.get("/history")
def getHistory(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return getCompletionHistory(db, currentUser.id)