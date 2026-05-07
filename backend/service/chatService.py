from sqlalchemy.orm import Session

from backend.models.chat import ChatHistory
from backend.models.onboarding import UserMentalProfile

from backend.service.aiTextService import analyzeTextEmotion
from backend.service.llmService import generateLlamaReply
from backend.service.riskService import calculateRiskScore
from backend.service.emojiService import detectEmojiEmotions
from backend.service.conversationBrainService import analyzeConversation
from backend.service.emotionTimelineService import buildEmotionTimelineSummary
from backend.service.crisisService import analyzeCrisis
from backend.service.memoryService import (
    updateLongTermMemory,
    getRelevantMemories,
    getPersonalityProfile,
    formatPersonalityProfile,
    decayMemories
)
from backend.service.personalityStyleService import (
    detectPersonalityStyle,
    formatPersonalityStyle
)


def getEmotionIntensity(confidence: float):
    if confidence > 0.85:
        return "high"
    elif confidence > 0.6:
        return "medium"
    return "low"


def shouldEscalate(db: Session, user_id: int):
    recent = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(5)
        .all()
    )

    negative = 0

    for chat in recent:
        if chat.emotion in ["fear", "sadness", "grief", "nervousness"]:
            negative += 1

    return negative >= 3


def getUserProfile(db: Session, user_id: int):
    return (
        db.query(UserMentalProfile)
        .filter(UserMentalProfile.user_id == user_id)
        .first()
    )


def cleanMemoryText(text: str, max_len: int = 120):
    if not text:
        return ""

    cleaned = (
        text.replace("SynthMind:", "")
        .replace("Assistant:", "")
        .replace("User:", "")
        .replace("|", " ")
        .replace("\n", " ")
        .strip()
    )

    return cleaned[:max_len]


def getRecentChatMemory(db: Session, user_id: int, limit: int = 4):
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
        userMsg = cleanMemoryText(chat.message, 90)
        replySummary = cleanMemoryText(chat.response, 120)

        if userMsg:
            memoryItems.append(f"Recent user message: {userMsg}")

        if replySummary:
            memoryItems.append(f"Recent assistant reply summary: {replySummary}")

    return "\n".join(memoryItems)


def buildConversationState(
    db: Session,
    user_id: int,
    message: str,
    emotion: str,
    brain: dict
):
    recentChats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(3)
        .all()
    )

    recentEmotions = [chat.emotion for chat in recentChats if chat.emotion]

    msg = message.lower()

    topic = "general"

    if "exam" in msg:
        topic = "exam"
    elif "interview" in msg:
        topic = "interview"
    elif "anxiety" in msg:
        topic = "anxiety"
    elif "scared" in msg:
        topic = "fear"

    emotionalMode = emotion in ["fear", "sadness", "grief", "nervousness"]

    return {
        "intent": brain.get("intent", "normal"),
        "emotion": emotion,
        "recentEmotions": recentEmotions,
        "emotionalMode": emotionalMode,
        "topic": topic
    }


def prepareChatContext(db: Session, user_id: int, message: str):
    emotionData = analyzeTextEmotion(message)
    emojiEmotions = detectEmojiEmotions(message)

    emotionIntensity = getEmotionIntensity(emotionData["confidence"])

    riskData = calculateRiskScore(db, user_id)
    riskLevel = riskData["final_risk"]

    brain = analyzeConversation(
        message=message,
        emotion=emotionData["topEmotion"],
        risk=riskLevel
    )

    profile = getUserProfile(db, user_id)

    profileText = ""

    if profile:
        profileText = f"""
User Mental Profile:
- Stress: {profile.stress_score}
- Wellness: {profile.wellness_score}
- Emotion: {profile.emotional_state}
- Support: {profile.support_level}
- Risk: {profile.risk_level}
- Personality: {profile.personality_summary}
"""

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

    personalityStyle = detectPersonalityStyle(
        profileText=profileText,
        memoryText=personalityText,
        brain=brain
    )

    personalityStyleText = formatPersonalityStyle(personalityStyle)

    timelineSummary = buildEmotionTimelineSummary(db, user_id)

    escalate = shouldEscalate(db, user_id)

    memory = f"""
Recent conversation summary:
{shortMemory}

Relevant long-term memory:
{longMemory}

{profileText}

Memory Personality:
{personalityText}

Adaptive Personality:
{personalityStyleText}

Timeline:
{timelineSummary}

Conversation State:
{conversationState}

Escalation: {escalate}
"""

    if not brain["useMemory"]:
        memory = f"""
{profileText}

Adaptive Personality:
{personalityStyleText}

Timeline:
{timelineSummary}
"""

    return {
        "emotionData": emotionData,
        "emojiEmotions": emojiEmotions,
        "riskLevel": riskLevel,
        "brain": brain,
        "memory": memory,
        "emotionIntensity": emotionIntensity,
        "escalate": escalate,
        "personalityStyle": personalityStyle
    }


def process_chat(db: Session, user_id: int, message: str, mode: str):
    crisis = analyzeCrisis(db, user_id, message)

    if crisis["risk_level"] in ["HIGH", "CRITICAL"]:
        chat = ChatHistory(
            user_id=user_id,
            message=message,
            response=crisis["response"],
            mode="crisis",
            emotion="crisis",
            confidence="1.0"
        )

        db.add(chat)
        db.commit()
        db.refresh(chat)

        return {
            "reply": crisis["response"],
            "emotion": "crisis",
            "riskLevel": crisis["risk_level"],
            "crisisDetected": True,
            "reason": crisis["reason"]
        }

    prepared = prepareChatContext(db, user_id, message)

    reply = generateLlamaReply(
        message=message,
        emotion=prepared["emotionData"]["topEmotion"],
        intensity=prepared["emotionIntensity"],
        memory=prepared["memory"],
        risk=prepared["riskLevel"],
        brain=prepared["brain"],
        escalate=prepared["escalate"]
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
        "riskLevel": prepared["riskLevel"],
        "personalityStyle": prepared["personalityStyle"],
        "crisisDetected": False
    }


def process_chat_stream(db: Session, user_id: int, message: str, mode: str):
    return prepareChatContext(db, user_id, message)