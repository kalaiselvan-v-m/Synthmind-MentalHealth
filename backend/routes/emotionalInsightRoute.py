from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.emotionalInsightService import buildEmotionalInsights

router = APIRouter(prefix="/emotional-insights", tags=["Emotional Insights"])


@router.get("")
def getEmotionalInsights(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return buildEmotionalInsights(db, currentUser.id)