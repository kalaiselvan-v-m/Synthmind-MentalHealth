from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.habitSuggestionService import buildHabitSuggestions

router = APIRouter(prefix="/habits", tags=["Habit Suggestions"])


@router.get("")
def getHabits(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return buildHabitSuggestions(db, currentUser.id)