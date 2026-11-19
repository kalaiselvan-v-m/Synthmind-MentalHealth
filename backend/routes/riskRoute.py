from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.riskService import calculateRiskScore

router = APIRouter(prefix="/risk", tags=["Risk Prediction"])


@router.get("")
def getRiskPrediction(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    return calculateRiskScore(db, currentUser.id)
