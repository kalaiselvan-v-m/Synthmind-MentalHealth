from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.service.riskService import calculateRiskScore

router = APIRouter(prefix="/risk", tags=["Risk Prediction"])


@router.get("/{user_id}")
def getRiskPrediction(user_id: int, db: Session = Depends(get_db)):
    return calculateRiskScore(db, user_id)