from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User

from backend.service.profileService import (
    getUserProfileData,
    clearChatHistory,
    clearJournal
)

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("")
def getProfile(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return getUserProfileData(db, currentUser.id)


@router.delete("/chat")
def deleteChat(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return clearChatHistory(db, currentUser.id)


@router.delete("/journal")
def deleteJournalEntries(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return clearJournal(db, currentUser.id)