from email import message

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
from backend.service.emotionalFlowService import buildEmotionalFlow
from backend.service.communicationStyleService import detectCommunicationStyle
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
    # -----------------------------
    # FAST EMOTION ANALYSIS
    # -----------------------------
    emotionData = analyzeTextEmotion(message)

    emotion = emotionData["topEmotion"]
    confidence = emotionData["confidence"]

    emotionIntensity = getEmotionIntensity(confidence)

    # -----------------------------
    # LIGHTWEIGHT RISK
    # -----------------------------
    riskData = calculateRiskScore(db, user_id)
    riskLevel = riskData["final_risk"]

    # -----------------------------
    # CONVERSATION BRAIN
    # -----------------------------
    brain = analyzeConversation(
        message=message,
        emotion=emotion,
        risk=riskLevel
    )

    # -----------------------------
    # USER PROFILE
    # -----------------------------
    profile = getUserProfile(db, user_id)

    profileText = ""

    if profile:
        profileText = f"""
Stress: {profile.stress_score}
Wellness: {profile.wellness_score}
Emotion: {profile.emotional_state}
Support: {profile.support_level}
"""

    # -----------------------------
    # SHORT MEMORY ONLY
    # -----------------------------
    shortMemory = getRecentChatMemory(
        db,
        user_id,
        limit=2
    )

    # -----------------------------
    # REDUCED LONG MEMORY
    # -----------------------------
    longMemory = getRelevantMemories(
        db,
        user_id,
        message
    )

    if longMemory:
        longMemory = longMemory[:350]

    # -----------------------------
    # LIGHT PERSONALITY SYSTEM
    # -----------------------------
    personalityProfile = getPersonalityProfile(
        db,
        user_id
    )

    personalityText = ""

    if personalityProfile:
        personalityText = formatPersonalityProfile(
            personalityProfile
        )[:250]

    # -----------------------------
    # FAST PERSONALITY STYLE
    # -----------------------------
    personalityStyle = {
        "style": "Emotionally Supportive Friend",
        "tone": "natural, emotionally aware, conversational"
    }

    personalityStyleText = """
Emotionally supportive, conversational, calm and natural.
Respond according to the user's emotional tone.
Avoid robotic or overly formal language.
"""

    # -----------------------------
    # SHORT TIMELINE
    # -----------------------------
    try:
        timelineSummary = buildEmotionTimelineSummary(
            db,
            user_id
        )

        timelineSummary = timelineSummary[:250]

    except:
        timelineSummary = ""

    # -----------------------------
    # ESCALATION CHECK
    # -----------------------------
    escalate = shouldEscalate(
        db,
        user_id
    )

    # -----------------------------
    # CONVERSATION STATE
    # -----------------------------
    conversationState = buildConversationState(
        db=db,
        user_id=user_id,
        message=message,
        emotion=emotion,
        brain=brain
    )
    communicationStyle = detectCommunicationStyle(message)

    recentEmotions = conversationState.get("recentEmotions", [])

    emotionalFlow = buildEmotionalFlow(
            recentEmotions=recentEmotions,
            message=message
        )

    # -----------------------------
    # FINAL MEMORY CONTEXT
    # -----------------------------
    memory = f"""
USER PROFILE:
{profileText}

RECENT CONVERSATION:
{shortMemory}

IMPORTANT MEMORY:
{longMemory}

PERSONALITY:
{personalityText}

EMOTIONAL FLOW:
{emotionalFlow}

COMMUNICATION STYLE:
{communicationStyle}

COMMUNICATION STYLE:
{personalityStyleText}

EMOTIONAL TIMELINE:
{timelineSummary}

CURRENT STATE:
{conversationState}

IMPORTANT RULES:
- Speak naturally
- Match the user's vibe
- Be emotionally intelligent
- Don't hallucinate facts
- Don't invent memories
- Keep responses human
- Avoid repetitive therapy language
"""

    # -----------------------------
    # LOW MEMORY MODE
    # -----------------------------
    if not brain["useMemory"]:
        memory = f"""
USER PROFILE:
{profileText}

COMMUNICATION STYLE:
{personalityStyleText}

CURRENT STATE:
{conversationState}

RULES:
- Be natural
- Be emotionally aware
- Keep responses conversational
"""

    return {
        "emotionData": emotionData,
        "emojiEmotions": [],
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