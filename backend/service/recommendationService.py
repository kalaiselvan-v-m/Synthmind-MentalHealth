from sqlalchemy.orm import Session

from backend.models.chat import ChatHistory
from backend.models.mood import Mood
from backend.service.riskService import calculateRiskScore
from backend.service.emojiService import detectEmojiEmotions


def getLatestMood(db: Session, user_id: int):
    mood = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.created_at.desc())
        .first()
    )

    return mood.mood if mood else "Unknown"


def getLatestChatEmotion(db: Session, user_id: int):
    chat = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .first()
    )

    if not chat:
        return "neutral", []

    emojiEmotions = detectEmojiEmotions(chat.message)

    return chat.emotion or "neutral", emojiEmotions


def buildRecommendations(emotion: str, emojiEmotions: list, mood: str, risk: str):
    recommendations = []

    combinedSignals = [emotion] + emojiEmotions

    if "nervousness" in combinedSignals or "fear" in combinedSignals:
        recommendations.extend([
            "Try 4-7-8 breathing for 2 minutes.",
            "Write down the exact thought that is making you anxious.",
            "Use the 5-4-3-2-1 grounding technique."
        ])

    if "sadness" in combinedSignals or "grief" in combinedSignals:
        recommendations.extend([
            "Write one small thing you wish someone understood about you.",
            "Listen to calming music for 5 minutes.",
            "Do one tiny activity like drinking water or stepping outside."
        ])

    if "anger" in combinedSignals:
        recommendations.extend([
            "Pause for 60 seconds before responding to anyone.",
            "Write what triggered your anger without judging yourself.",
            "Try relaxing your shoulders and breathing slowly."
        ])

    if "joy" in combinedSignals or "love" in combinedSignals:
        recommendations.extend([
            "Save this positive moment in your journal.",
            "Share this good feeling with someone you trust.",
            "Do one more small thing that supports this mood."
        ])

    if "tired" in combinedSignals:
        recommendations.extend([
            "Take a short screen break.",
            "Drink water and rest your eyes for 2 minutes.",
            "Try a small low-effort task instead of forcing productivity."
        ])

    if "overwhelmed" in combinedSignals:
        recommendations.extend([
            "Write only the next one thing you need to do.",
            "Try a 2-minute grounding pause.",
            "Break the problem into one small step."
        ])

    if mood in ["Low", "Overwhelmed"]:
        recommendations.append(
            "Do a 3-minute check-in: What am I feeling? What do I need right now?"
        )

    if risk == "High":
        recommendations.append(
            "If this feeling continues, consider reaching out to a trusted person or professional support."
        )
    elif risk == "Medium":
        recommendations.append(
            "Try a short CBT reflection: Is this thought 100% true, or is there another view?"
        )

    if not recommendations:
        recommendations = [
            "Take a short mindful pause.",
            "Write one sentence about how you feel right now.",
            "Do one small self-care action."
        ]

    return list(dict.fromkeys(recommendations))


def getPersonalizedRecommendations(db: Session, user_id: int):
    riskData = calculateRiskScore(db, user_id)
    risk = riskData["final_risk"]

    mood = getLatestMood(db, user_id)
    emotion, emojiEmotions = getLatestChatEmotion(db, user_id)

    recommendations = buildRecommendations(
        emotion=emotion,
        emojiEmotions=emojiEmotions,
        mood=mood,
        risk=risk
    )

    return {
        "user_id": user_id,
        "current_emotion": emotion,
        "emoji_emotions": emojiEmotions,
        "latest_mood": mood,
        "risk_level": risk,
        "recommendations": recommendations,
        "note": "These are AI wellness suggestions, not medical diagnosis."
    }