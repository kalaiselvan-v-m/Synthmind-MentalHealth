from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User

from backend.schemas.journalSchema import CreateJournalRequest
from backend.service.journalService import createJournalEntry, getJournalEntries

router = APIRouter(prefix="/journal", tags=["Journal"])


@router.post("")
def createJournal(
    data: CreateJournalRequest,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return createJournalEntry(db, currentUser.id, data.content)


@router.get("")
def getJournals(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return getJournalEntries(db, currentUser.id)