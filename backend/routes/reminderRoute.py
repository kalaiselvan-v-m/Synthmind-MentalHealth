from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.reminderService import generateSmartReminder

router = APIRouter(prefix="/reminder", tags=["Reminder"])


@router.get("")
def getReminder(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return {
        "message": generateSmartReminder(db, currentUser.id)
    }