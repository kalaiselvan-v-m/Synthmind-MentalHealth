from sqlalchemy.orm import Session

from backend.models.chat import ChatHistory
from backend.service.aiTextService import analyzeTextEmotion
from backend.service.llmService import generateLlamaReply
from backend.service.riskService import calculateRiskScore
from backend.service.emojiService import detectEmojiEmotions
from backend.service.conversationBrainService import analyzeConversation
from backend.service.memoryService import (
    updateLongTermMemory,
    getRelevantMemories,
    getPersonalityProfile,
    formatPersonalityProfile,
    decayMemories
)


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
        memoryItems.append(f"User: {chat.message}")
        memoryItems.append(f"SynthMind: {chat.response}")

    return " | ".join(memoryItems)


def buildConversationState(db: Session, user_id: int, message: str, emotion: str, brain: dict):
    recentChats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(3)
        .all()
    )

    recentEmotions = [chat.emotion for chat in recentChats if chat.emotion]
    recentModes = [chat.mode for chat in recentChats if chat.mode]

    msg = message.lower()

    topic = "general"

    if "exam" in msg or "test" in msg:
        topic = "exam"
    elif "interview" in msg:
        topic = "interview"
    elif "anxiety" in msg or "anxious" in msg:
        topic = "anxiety"
    elif "scared" in msg or "afraid" in msg:
        topic = "fear"

    emotionalMode = False

    if emotion in ["fear", "sadness", "grief", "nervousness", "remorse", "disappointment"]:
        emotionalMode = True

    if "emotional_support" in recentModes:
        emotionalMode = True

    return {
        "currentIntent": brain.get("intent", "normal"),
        "currentEmotion": emotion,
        "recentEmotions": recentEmotions,
        "recentModes": recentModes,
        "emotionalMode": emotionalMode,
        "topic": topic,
        "seriousness": brain.get("seriousness", "light")
    }


def formatConversationState(state: dict):
    return f"""
Conversation state:
- Current intent: {state["currentIntent"]}
- Current emotion: {state["currentEmotion"]}
- Recent emotions: {state["recentEmotions"]}
- Recent modes: {state["recentModes"]}
- Emotional mode active: {state["emotionalMode"]}
- Topic: {state["topic"]}
- Seriousness: {state["seriousness"]}
"""


def prepareChatContext(db: Session, user_id: int, message: str):
    emotionData = analyzeTextEmotion(message)
    emojiEmotions = detectEmojiEmotions(message)

    riskData = calculateRiskScore(db, user_id)
    riskLevel = riskData["final_risk"]

    brain = analyzeConversation(
        message=message,
        emotion=emotionData["topEmotion"],
        risk=riskLevel
    )

    conversationState = buildConversationState(
        db=db,
        user_id=user_id,
        message=message,
        emotion=emotionData["topEmotion"],
        brain=brain
    )

    shortMemory = getRecentChatMemory(db, user_id)
    longMemory = getRelevantMemories(db, user_id, message)

    personalityProfile = getPersonalityProfile(db, user_id)
    personalityText = formatPersonalityProfile(personalityProfile)
    stateText = formatConversationState(conversationState)

    memory = f"""
Short-term memory:
{shortMemory}

Relevant long-term memory:
{longMemory}

User personality profile:
{personalityText}

{stateText}
"""

    if not brain["useMemory"]:
        memory = f"""
User personality profile:
{personalityText}

{stateText}
"""

    return {
        "emotionData": emotionData,
        "emojiEmotions": emojiEmotions,
        "riskLevel": riskLevel,
        "brain": brain,
        "memory": memory,
        "personalityProfile": personalityProfile,
        "conversationState": conversationState
    }


def process_chat(db: Session, user_id: int, message: str, mode: str):
    prepared = prepareChatContext(db, user_id, message)

    reply = generateLlamaReply(
        message=message,
        emotion=prepared["emotionData"]["topEmotion"],
        mode=prepared["brain"]["intent"],
        memory=prepared["memory"],
        risk=prepared["riskLevel"],
        brain=prepared["brain"]
    )

    chat = ChatHistory(
        user_id=user_id,
        message=message,
        response=reply,
        mode=prepared["brain"]["intent"],
        emotion=prepared["emotionData"]["topEmotion"],
        confidence=str(prepared["emotionData"]["confidence"])
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    updateLongTermMemory(db, user_id, message)
    decayMemories(db, user_id)

    return {
        "reply": reply,
        "emotion": prepared["emotionData"]["topEmotion"],
        "emojiEmotions": prepared["emojiEmotions"],
        "confidence": prepared["emotionData"]["confidence"],
        "riskLevel": prepared["riskLevel"],
        "conversationBrain": prepared["brain"],
        "conversationState": prepared["conversationState"],
        "personalityProfile": prepared["personalityProfile"],
        "memoryUsed": prepared["brain"]["useMemory"]
    }


def process_chat_stream(db: Session, user_id: int, message: str, mode: str):
    return prepareChatContext(db, user_id, message)