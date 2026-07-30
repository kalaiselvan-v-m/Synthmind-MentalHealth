from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.service.recoveryIntelligenceService import (
    updateRecoveryStatus,
    getRecoveryOverview
)

router = APIRouter(
    prefix="/recovery-intelligence",
    tags=["Recovery Intelligence"]
)


@router.get("")
def recoveryOverview(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return getRecoveryOverview(db, currentUser.id)


@router.post("/update")
def updateRecovery(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return updateRecoveryStatus(db, currentUser.id)