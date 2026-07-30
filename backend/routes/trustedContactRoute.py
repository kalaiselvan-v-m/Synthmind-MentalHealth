from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User
from backend.models.crisisSupportAction import CrisisSupportAction
from backend.service.trustedContactService import (
    getTrustedContact,
    saveTrustedContact,
    deleteTrustedContact
)

router = APIRouter(prefix="/trusted-contact", tags=["Trusted Contact"])


class TrustedContactRequest(BaseModel):
    contact_name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    relationship: Optional[str] = None
    alerts_enabled: bool = True
    notify_on_critical: bool = True


@router.get("")
def fetchTrustedContact(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    contact = getTrustedContact(db, currentUser.id)

    if not contact:
        return None

    return {
        "id": contact.id,
        "contact_name": contact.contact_name,
        "contact_phone": contact.contact_phone,
        "contact_email": contact.contact_email,
        "relationship": contact.relationship,
        "alerts_enabled": contact.alerts_enabled,
        "notify_on_critical": contact.notify_on_critical,
        "created_at": contact.created_at
    }


@router.post("")
def createOrUpdateTrustedContact(
    data: TrustedContactRequest,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    contact = saveTrustedContact(
        db=db,
        user_id=currentUser.id,
        contact_name=data.contact_name,
        contact_phone=data.contact_phone,
        contact_email=data.contact_email,
        relationship=data.relationship,
        alerts_enabled=data.alerts_enabled,
        notify_on_critical=data.notify_on_critical
    )

    return {
        "message": "Trusted contact saved",
        "contact": {
            "id": contact.id,
            "contact_name": contact.contact_name,
            "contact_phone": contact.contact_phone,
            "contact_email": contact.contact_email,
            "relationship": contact.relationship,
            "alerts_enabled": contact.alerts_enabled,
            "notify_on_critical": contact.notify_on_critical,
            "created_at": contact.created_at
        }
    }


@router.delete("")
def removeTrustedContact(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return deleteTrustedContact(db, currentUser.id)

@router.post("/notify-preview")
def notifyTrustedContactPreview(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    contact = getTrustedContact(db, currentUser.id)

    if not contact:
        return {
            "can_notify": False,
            "message": "No trusted contact found. Please add one in Profile first."
        }

    if not contact.alerts_enabled or not contact.notify_on_critical:
        return {
            "can_notify": False,
            "message": "Crisis support alerts are disabled in your safety settings."
        }

    preview_message = (
        f"Hi {contact.contact_name}, someone who trusts you may be going through "
        "a difficult emotional moment right now. A gentle check-in from you could really help."
    )
    action = CrisisSupportAction(
    user_id=currentUser.id,
    risk_level="CRITICAL",
    action_type="trusted_contact_preview",
    status="previewed",
    details=preview_message
    )

    db.add(action)
    db.commit()

    return {
        "can_notify": True,
        "contact_name": contact.contact_name,
        "contact_phone": contact.contact_phone,
        "contact_email": contact.contact_email,
        "message": preview_message
    }