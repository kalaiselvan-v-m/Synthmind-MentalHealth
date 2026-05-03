from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.service.recommendationService import getPersonalizedRecommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{user_id}")
def getRecommendations(user_id: int, db: Session = Depends(get_db)):
    return getPersonalizedRecommendations(db, user_id)