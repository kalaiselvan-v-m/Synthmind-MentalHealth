from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.recoveryPlanService import buildRecoveryPlan

router = APIRouter(prefix="/recovery-plan", tags=["Recovery Plan"])


@router.get("")
def getRecoveryPlan(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser),
):
    return buildRecoveryPlan(db, currentUser.id)
