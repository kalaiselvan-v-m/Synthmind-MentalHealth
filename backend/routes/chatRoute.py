from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.chatSchema import ChatRequest
from backend.service.chatService import process_chat, process_chat_stream
from backend.service.llmService import streamLlamaReply
from backend.service.memoryService import updateLongTermMemory
from backend.models.chat import ChatHistory
from backend.dependencies.authDependency import getCurrentUser
from backend.models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/send")
def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return process_chat(db, currentUser.id, data.message, data.mode)


@router.post("/stream")
def chatStream(
    data: ChatRequest,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    prepared = process_chat_stream(db, currentUser.id, data.message, data.mode)

    def eventGenerator():
        fullReply = ""

        for chunk in streamLlamaReply(
            message=data.message,
            emotion=prepared["emotionData"]["topEmotion"],
            memory=prepared["memory"],
            risk=prepared["riskLevel"],
            brain=prepared["brain"]
        ):
            fullReply += chunk
            yield chunk

        chat = ChatHistory(
            user_id=currentUser.id,
            message=data.message,
            response=fullReply,
            mode=prepared["brain"]["intent"],
            emotion=prepared["emotionData"]["topEmotion"],
            confidence=str(prepared["emotionData"]["confidence"])
        )

        db.add(chat)
        db.flush()
        db.commit()

        updateLongTermMemory(db, currentUser.id, data.message)

    return StreamingResponse(eventGenerator(), media_type="text/plain")


@router.get("/latest-meta")
def getLatestChatMeta(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    chat = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == currentUser.id)
        .order_by(ChatHistory.created_at.desc())
        .first()
    )

    if not chat:
        return {
            "emotion": "neutral",
            "riskLevel": "Low",
            "mode": "normal",
            "confidence": "0.0"
        }

    from backend.service.riskService import calculateRiskScore
    riskData = calculateRiskScore(db, currentUser.id)

    return {
        "emotion": chat.emotion or "neutral",
        "riskLevel": riskData["final_risk"] or "Low",
        "mode": chat.mode or "normal",
        "confidence": chat.confidence or "0.0"
    }


@router.get("/history")
def get_chat_history(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == currentUser.id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )


@router.delete("/history")
def delete_history(
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    db.query(ChatHistory).filter(ChatHistory.user_id == currentUser.id).delete()
    db.commit()
    return {"message": "Chat history cleared"}