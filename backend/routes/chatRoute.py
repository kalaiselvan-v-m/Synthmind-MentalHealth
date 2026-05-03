from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.chatSchema import ChatRequest
from backend.service.chatService import process_chat
from backend.models.chat import ChatHistory

router = APIRouter(prefix="/chat", tags=["Chat"])


# ✅ Send message
@router.post("/send")
def chat(data: ChatRequest, db: Session = Depends(get_db)):
    result = process_chat(db, data.user_id, data.message, data.mode)
    return result


# ✅ Chat history
@router.get("/history/{user_id}")
def get_chat_history(user_id: int, db: Session = Depends(get_db)):
    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )
    return chats


# ✅ Delete history
@router.delete("/history/{user_id}")
def delete_history(user_id: int, db: Session = Depends(get_db)):
    db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
    db.commit()
    return {"message": "Chat history cleared"}