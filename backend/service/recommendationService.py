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


def getRecentChats(db: Session, user_id: int, limit: int = 8):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )


def detectRecentThemes(chats):
    text = " ".join(
        [
            (chat.message or "").lower()
            for chat in chats
        ]
    )

    themes = []

    if any(word in text for word in [
        "interview",
        "placement",
        "job",
        "career"
    ]):
        themes.append("career_pressure")

    if any(word in text for word in [
        "exam",
        "assignment",
        "test",
        "deadline",
        "study"
    ]):
        themes.append("academic_pressure")

    if any(word in text for word in [
        "alone",
        "lonely",
        "invisible",
        "nobody cares",
        "no one cares",
        "not important"
    ]):
        themes.append("emotional_disconnection")

    if any(word in text for word in [
        "failed",
        "failure",
        "useless",
        "not good enough",
        "worthless",
        "losing myself",
        "not myself"
    ]):
        themes.append("self_doubt")

    if any(word in text for word in [
        "tired",
        "exhausted",
        "drained",
        "burned out",
        "overwhelmed"
    ]):
        themes.append("mental_exhaustion")

    if any(word in text for word in [
        "sleep",
        "insomnia",
        "awake",
        "rest"
    ]):
        themes.append("sleep_rest")

    return list(dict.fromkeys(themes))


def buildWellnessFocus(
    emotion: str,
    mood: str,
    risk: str,
    themes: list
):
    if risk == "High":
        return {
            "title": "Take things gently right now.",
            "reason": (
                "Your recent signals look emotionally heavier, so the focus "
                "should be safety, support, and small steps."
            )
        }

    if "career_pressure" in themes:
        return {
            "title": "Reduce interview pressure.",
            "reason": (
                "Interviews or career thoughts seem to be part of your recent stress."
            )
        }

    if "academic_pressure" in themes:
        return {
            "title": "Make academic pressure feel smaller.",
            "reason": (
                "Study, exams, or deadlines appear in your recent emotional pattern."
            )
        }

    if "emotional_disconnection" in themes:
        return {
            "title": "Feel a little less alone.",
            "reason": (
                "There are signs of emotional disconnection in your recent conversations."
            )
        }

    if "self_doubt" in themes:
        return {
            "title": "Be softer with yourself.",
            "reason": (
                "You’ve sounded self-critical recently, so the goal is to reduce harsh self-talk."
            )
        }

    if "mental_exhaustion" in themes:
        return {
            "title": "Lower the mental load.",
            "reason": (
                "Your recent messages suggest tiredness or emotional overload."
            )
        }

    if emotion in ["fear", "nervousness"]:
        return {
            "title": "Slow the pressure down.",
            "reason": (
                "Your current emotional signal looks anxious or tense."
            )
        }

    if emotion in ["sadness", "grief"]:
        return {
            "title": "Give yourself more gentleness.",
            "reason": (
                "Your current emotional signal feels heavier than usual."
            )
        }

    if mood in ["Low", "Overwhelmed"]:
        return {
            "title": "Support your mood softly.",
            "reason": (
                "Your latest mood check-in suggests you may need lighter routines."
            )
        }

    return {
        "title": "Protect your mental balance.",
        "reason": (
            "Your recent signals look relatively stable, so the focus is consistency."
        )
    }


def buildRecommendations(
    emotion: str,
    emojiEmotions: list,
    mood: str,
    risk: str,
    themes: list
):
    recommendations = []

    combinedSignals = [emotion] + emojiEmotions

    if "career_pressure" in themes:
        recommendations.extend([
            "Write down 3 interview questions you fear most, then prepare one calm answer for each.",
            "Do a 5-minute mock answer practice without judging yourself.",
            "Before interview prep, take 3 slow breaths and remind yourself: preparation is progress."
        ])

    if "academic_pressure" in themes:
        recommendations.extend([
            "Pick only one academic task to finish first.",
            "Use a 25-minute focus timer and stop when it ends.",
            "Write the deadline or exam worry clearly, then break it into one small action."
        ])

    if "emotional_disconnection" in themes:
        recommendations.extend([
            "Send one simple message to someone safe, even if it is just 'hey'.",
            "Write one line about what you wish someone understood about you.",
            "Spend a few minutes somewhere you feel less emotionally crowded."
        ])

    if "self_doubt" in themes:
        recommendations.extend([
            "Write one thing you did try, even if the result was not perfect.",
            "Replace one harsh self-thought with a more fair version.",
            "Take a small break before judging yourself again."
        ])

    if "mental_exhaustion" in themes:
        recommendations.extend([
            "Choose a low-effort task instead of forcing productivity.",
            "Take a short screen break and rest your eyes.",
            "Drink water and sit quietly for two minutes."
        ])

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

    return list(dict.fromkeys(recommendations))[:8]


def getPersonalizedRecommendations(db: Session, user_id: int):
    riskData = calculateRiskScore(db, user_id)
    risk = riskData["final_risk"]

    mood = getLatestMood(db, user_id)
    emotion, emojiEmotions = getLatestChatEmotion(db, user_id)

    recentChats = getRecentChats(db, user_id)
    recentThemes = detectRecentThemes(recentChats)

    wellnessFocus = buildWellnessFocus(
        emotion=emotion,
        mood=mood,
        risk=risk,
        themes=recentThemes
    )

    recommendations = buildRecommendations(
        emotion=emotion,
        emojiEmotions=emojiEmotions,
        mood=mood,
        risk=risk,
        themes=recentThemes
    )

    musicRecommendations = buildMusicRecommendations(
    emotion=emotion,
    mood=mood,
    risk=risk,
    themes=recentThemes
  )  

    return {
        "user_id": user_id,
        "current_emotion": emotion,
        "emoji_emotions": emojiEmotions,
        "latest_mood": mood,
        "risk_level": risk,
        "recent_themes": recentThemes,
        "wellness_focus": wellnessFocus,
        "recommendations": recommendations,
        "music_recommendations": musicRecommendations,
        "note": "These are AI wellness suggestions, not medical diagnosis."
    }

def buildMusicRecommendations(
    emotion: str,
    mood: str,
    risk: str,
    themes: list
):
    playlists = []

    if risk == "High":
        playlists.append({
            "title": "Soft grounding sounds",
            "description": "Gentle ambient music to reduce emotional intensity.",
            "type": "grounding"
        })

    if emotion in ["sadness", "grief"]:
        playlists.append({
            "title": "Gentle healing music",
            "description": "Slow calming tracks for emotional heaviness.",
            "type": "healing"
        })

    if emotion in ["fear", "nervousness"]:
        playlists.append({
            "title": "Calm anxiety relief",
            "description": "Soft focus sounds to slow racing thoughts.",
            "type": "anxiety"
        })

    if "mental_exhaustion" in themes:
        playlists.append({
            "title": "Deep mental reset",
            "description": "Low-stimulation sounds for emotional recovery.",
            "type": "reset"
        })

    if emotion in ["joy", "love"]:
        playlists.append({
            "title": "Feel-good energy",
            "description": "Positive uplifting music for emotional momentum.",
            "type": "uplifting"
        })

    if not playlists:
        playlists.append({
            "title": "Balanced focus music",
            "description": "Gentle background music for emotional balance.",
            "type": "focus"
        })

    return playlists[:3]