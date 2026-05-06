from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.weeklyReportService import generateWeeklyReport

router = APIRouter(prefix="/weekly-report", tags=["Weekly Report"])


@router.get("")
def getWeeklyReport(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return generateWeeklyReport(db, currentUser.id)