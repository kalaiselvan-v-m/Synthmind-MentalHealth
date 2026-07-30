from sqlalchemy.orm import Session

from backend.models.trustedContact import TrustedContact


def getTrustedContact(db: Session, user_id: int):
    contact = (
        db.query(TrustedContact)
        .filter(TrustedContact.user_id == user_id)
        .first()
    )

    return contact


def saveTrustedContact(
    db: Session,
    user_id: int,
    contact_name: str,
    contact_phone: str = None,
    contact_email: str = None,
    relationship: str = None,
    alerts_enabled: bool = True,
    notify_on_critical: bool = True
):
    contact = getTrustedContact(db, user_id)

    if contact:
        contact.contact_name = contact_name
        contact.contact_phone = contact_phone
        contact.contact_email = contact_email
        contact.relationship = relationship
        contact.alerts_enabled = alerts_enabled
        contact.notify_on_critical = notify_on_critical
    else:
        contact = TrustedContact(
            user_id=user_id,
            contact_name=contact_name,
            contact_phone=contact_phone,
            contact_email=contact_email,
            relationship=relationship,
            alerts_enabled=alerts_enabled,
            notify_on_critical=notify_on_critical
        )

        db.add(contact)

    db.commit()
    db.refresh(contact)

    return contact


def deleteTrustedContact(db: Session, user_id: int):
    contact = getTrustedContact(db, user_id)

    if not contact:
        return {"message": "No trusted contact found"}

    db.delete(contact)
    db.commit()

    return {"message": "Trusted contact removed"}