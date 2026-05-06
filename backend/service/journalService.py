from sqlalchemy.orm import Session

from backend.models.journal import JournalEntry
from backend.models.chat import ChatHistory
from backend.service.aiTextService import analyzeTextEmotion
from backend.service.llmService import generateJournalInsight


def getRecentJournalContext(db: Session, user_id: int, limit: int = 3):
    recentChats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    if not recentChats:
        return ""

    contextItems = []

    for chat in reversed(recentChats):
        contextItems.append(f"Recent emotion: {chat.emotion}, message: {chat.message}")

    return " | ".join(contextItems)


def createJournalEntry(db: Session, user_id: int, content: str):
    emotionData = analyzeTextEmotion(content)

    memory = getRecentJournalContext(db, user_id)

    summary = generateJournalInsight(
        content=content,
        emotion=emotionData["topEmotion"],
        memory=memory
    )

    entry = JournalEntry(
        user_id=user_id,
        content=content,
        emotion=emotionData["topEmotion"],
        confidence=str(emotionData["confidence"]),
        ai_summary=summary
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


def getJournalEntries(db: Session, user_id: int):
    return (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == user_id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )