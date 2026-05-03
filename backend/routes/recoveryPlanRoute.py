from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.service.recoveryPlanService import buildRecoveryPlan

router = APIRouter(prefix="/recovery-plan", tags=["Recovery Plan"])


@router.get("/{user_id}")
def getRecoveryPlan(user_id: int, db: Session = Depends(get_db)):
    return buildRecoveryPlan(db, user_id)