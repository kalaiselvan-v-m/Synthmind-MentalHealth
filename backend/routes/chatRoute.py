
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.chatSchema import ChatRequest
from backend.service.chatService import process_chat, process_chat_stream
from backend.service.llmService import streamLlamaReply
from backend.service.memoryService import updateLongTermMemory
from backend.service.crisisService import analyzeCrisis
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
    return process_chat(
        db,
        currentUser.id,
        data.message,
        data.mode
    )


@router.post("/stream")
def chatStream(
    data: ChatRequest,
    db: Session = Depends(get_db),
    currentUser: User = Depends(getCurrentUser)
):
    prepared = process_chat_stream(
        db,
        currentUser.id,
        data.message,
        data.mode
    )

    # Analyze the current message exactly once.
    crisis = analyzeCrisis(
        db,
        currentUser.id,
        data.message
    )

    def eventGenerator():

        fullReply = ""

        # MEDIUM, HIGH and CRITICAL messages receive
        # their dedicated support response.
        if crisis["risk_level"] in [
            "MEDIUM",
            "HIGH",
            "CRITICAL"
        ]:

            crisisPayload = {
                "riskLevel": crisis["risk_level"],
                "crisisDetected": crisis["crisis_detected"],
                "response": crisis["response"]
            }

            yield "__CRISIS__" + json.dumps(crisisPayload) + "\n"

            fullReply = crisis["response"]

        else:

            # Normal conversation: stream the AI response.
            try:
                for chunk in streamLlamaReply(
                    message=data.message,
                    emotion=prepared["emotionData"]["topEmotion"],
                    intensity=prepared["emotionIntensity"],
                    memory=prepared["memory"],
                    risk=prepared["riskLevel"],
                    brain=prepared["brain"],
                    escalate=prepared["escalate"]
                ):
                    fullReply += chunk
                    yield chunk

            except Exception as error:
                print("STREAM ERROR:", str(error))

                fullReply = (
                    "I'm having trouble responding right now. "
                    "Please try again."
                )

                yield fullReply

        # Save the chat once, after generating its response.
        try:
            chatRecord = ChatHistory(
                user_id=currentUser.id,
                message=data.message,
                response=fullReply,
                mode=(
                    "crisis"
                    if crisis["risk_level"] in [
                        "HIGH",
                        "CRITICAL"
                    ]
                    else (
                        "emotional_support"
                        if crisis["risk_level"] == "MEDIUM"
                        else prepared["brain"]["intent"]
                    )
                ),
                emotion=(
                    "crisis"
                    if crisis["risk_level"] in [
                        "HIGH",
                        "CRITICAL"
                    ]
                    else prepared["emotionData"]["topEmotion"]
                ),
                confidence=(
                    "1.0"
                    if crisis["risk_level"] in [
                        "MEDIUM",
                        "HIGH",
                        "CRITICAL"
                    ]
                    else str(prepared["emotionData"]["confidence"])
                )
            )

            db.add(chatRecord)
            db.commit()

            if crisis["risk_level"] == "LOW":
                updateLongTermMemory(
                    db,
                    currentUser.id,
                    data.message
                )

        except Exception as error:
            db.rollback()
            print("POST STREAM SAVE ERROR:", str(error))

    return StreamingResponse(
        eventGenerator(),
        media_type="text/plain"
    )


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

    riskData = calculateRiskScore(
        db,
        currentUser.id
    )

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

    db.query(ChatHistory).filter(
        ChatHistory.user_id == currentUser.id
    ).delete()

    db.commit()

    return {
        "message": "Chat history cleared"
    }
