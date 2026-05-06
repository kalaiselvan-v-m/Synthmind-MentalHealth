from sqlalchemy.orm import Session

from backend.models.chat import ChatHistory
from backend.models.journal import JournalEntry
from backend.models.onboarding import UserMentalProfile


def getUserProfileData(db: Session, user_id: int):
    profile = (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )

    chatCount = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .count()
    )

    journalCount = (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .count()
    )

    return {
        "profile": profile,
        "chatCount": chatCount,
        "journalCount": journalCount
    }


def clearChatHistory(db: Session, user_id: int):
    db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
    db.commit()
    return {"message": "Chat history cleared"}


def clearJournal(db: Session, user_id: int):
    db.query(JournalEntry).filter(JournalEntry.user_id == user_id).delete()
    db.commit()
    return {"message": "Journal cleared"}