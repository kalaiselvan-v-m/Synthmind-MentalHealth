from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.service.recommendationService import getPersonalizedRecommendations
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("")
def getRecommendations(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return getPersonalizedRecommendations(db, currentUser.id)