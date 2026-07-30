from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.models.crisisSupportAction import CrisisSupportAction

router = APIRouter(
    prefix="/crisis-support",
    tags=["Crisis Support"]
)


@router.post("/grounding-complete")
def groundingComplete(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    action = CrisisSupportAction(
        user_id=currentUser.id,
        risk_level="HIGH",
        action_type="grounding_completed",
        status="completed",
        details="User completed grounding exercise."
    )

    db.add(action)
    db.commit()

    return {
        "message": "Grounding session saved."
    }