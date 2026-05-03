from sqlalchemy.orm import Session

from backend.models.chat import ChatHistory
from backend.service.aiTextService import analyzeTextEmotion
from backend.service.llmService import generateLlamaReply
from backend.service.riskService import calculateRiskScore
from backend.service.emojiService import detectEmojiEmotions


def getRecentChatMemory(db: Session, user_id: int, limit: int = 5):
    chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )

    chats = list(reversed(chats))

    memoryItems = []

    for chat in chats:
        memoryItems.append(chat.message)

    return " | ".join(memoryItems)


def process_chat(db: Session, user_id: int, message: str, mode: str):
    emotionData = analyzeTextEmotion(message)

    emojiEmotions = detectEmojiEmotions(message)

    memory = getRecentChatMemory(db, user_id)

    riskData = calculateRiskScore(db, user_id)
    riskLevel = riskData["final_risk"]

    reply = generateLlamaReply(
        message=message,
        emotion=emotionData["topEmotion"],
        mode=mode,
        memory=memory,
        risk=riskLevel
    )

    chat = ChatHistory(
        user_id=user_id,
        message=message,
        response=reply,
        mode=mode,
        emotion=emotionData["topEmotion"],
        confidence=str(emotionData["confidence"])
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {
        "reply": reply,
        "emotion": emotionData["topEmotion"],
        "emojiEmotions": emojiEmotions,
        "confidence": emotionData["confidence"],
        "riskLevel": riskLevel,
        "memoryUsed": True
    }