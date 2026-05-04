from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.models.userMemory import UserMemory
from backend.service.memoryLLMService import extractMemoryWithLLM


def fallbackExtractMemory(message: str):
    msg = message.lower()
    memories = []

    if "exam" in msg or "test" in msg:
        memories.append({
            "type": "stress_trigger",
            "key": "exam_stress",
            "value": "User may feel stressed about exams",
            "importance": 3
        })

    if "interview" in msg:
        memories.append({
            "type": "stress_trigger",
            "key": "interview_stress",
            "value": "User may feel nervous about interviews",
            "importance": 3
        })

    if "talk like a homie" in msg or "talk like a friend" in msg or "bro" in msg:
        memories.append({
            "type": "preference",
            "key": "casual_tone",
            "value": "User prefers casual friendly tone",
            "importance": 2
        })

    if "short reply" in msg or "reply short" in msg or "make it short" in msg:
        memories.append({
            "type": "preference",
            "key": "short_replies",
            "value": "User prefers short replies",
            "importance": 2
        })

    if "anxious" in msg or "anxiety" in msg:
        memories.append({
            "type": "emotion_pattern",
            "key": "anxiety_pattern",
            "value": "User has mentioned anxiety",
            "importance": 3
        })

    if "scared" in msg or "afraid" in msg:
        memories.append({
            "type": "emotion_pattern",
            "key": "fear_pattern",
            "value": "User has mentioned feeling scared",
            "importance": 3
        })

    return memories


def saveMemory(db: Session, user_id: int, memory: dict):
    if not memory.get("key") or not memory.get("value"):
        return None

    importance = memory.get("importance", 1)

    try:
        importance = int(importance)
    except Exception:
        importance = 1

    importance = max(1, min(importance, 3))

    existing = (
        db.query(UserMemory)
        .filter(
            UserMemory.user_id == user_id,
            UserMemory.memory_key == memory["key"]
        )
        .first()
    )

    if existing:
        existing.memory_type = memory.get("type", existing.memory_type)
        existing.memory_value = memory["value"]

        # Reinforcement: repeated memories become stronger.
        existing.importance = min(3, max(existing.importance, importance) + 1)

        db.commit()
        db.refresh(existing)
        return existing

    newMemory = UserMemory(
        user_id=user_id,
        memory_type=memory.get("type", "general"),
        memory_key=memory["key"],
        memory_value=memory["value"],
        importance=importance
    )

    db.add(newMemory)
    db.commit()
    db.refresh(newMemory)

    return newMemory


def updateLongTermMemory(db: Session, user_id: int, message: str):
    memories = []

    try:
        memories = extractMemoryWithLLM(message)
    except Exception as e:
        print("LLM memory extraction failed:", str(e))
        memories = []

    if not memories:
        memories = fallbackExtractMemory(message)

    savedMemories = []

    for memory in memories:
        saved = saveMemory(db, user_id, memory)
        if saved:
            savedMemories.append(saved)

    return savedMemories


def getRelevantMemories(db: Session, user_id: int, message: str, limit: int = 5):
    msg = message.lower()

    query = db.query(UserMemory).filter(UserMemory.user_id == user_id)

    if "exam" in msg or "test" in msg:
        query = query.filter(UserMemory.memory_key.contains("exam"))

    elif "interview" in msg:
        query = query.filter(UserMemory.memory_key.contains("interview"))

    elif "anxiety" in msg or "anxious" in msg:
        query = query.filter(UserMemory.memory_key.contains("anxiety"))

    elif "scared" in msg or "afraid" in msg:
        query = query.filter(UserMemory.memory_key.contains("fear"))

    else:
        query = query.order_by(UserMemory.importance.desc())

    memories = query.limit(limit).all()

    cleanMemories = []

    for memory in memories:
        if memory.memory_key in ["short_key", "mention"]:
            continue

        if "clear human-readable memory" in memory.memory_value.lower():
            continue

        cleanMemories.append(memory.memory_value)

    return " | ".join(cleanMemories)


def getPersonalityProfile(db: Session, user_id: int):
    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .order_by(UserMemory.importance.desc())
        .all()
    )

    preferences = []
    emotionalPatterns = []
    stressTriggers = []

    for memory in memories:
        if memory.memory_key in ["short_key", "mention"]:
            continue

        if "clear human-readable memory" in memory.memory_value.lower():
            continue

        if memory.memory_type == "preference":
            preferences.append(memory.memory_value)

        elif memory.memory_type == "emotion_pattern":
            emotionalPatterns.append(memory.memory_value)

        elif memory.memory_type == "stress_trigger":
            stressTriggers.append(memory.memory_value)

    return {
        "preferences": preferences[:5],
        "emotionalPatterns": emotionalPatterns[:5],
        "stressTriggers": stressTriggers[:5]
    }


def formatPersonalityProfile(profile: dict):
    parts = []

    if profile["preferences"]:
        parts.append("User preferences: " + " | ".join(profile["preferences"]))

    if profile["emotionalPatterns"]:
        parts.append("Emotional patterns: " + " | ".join(profile["emotionalPatterns"]))

    if profile["stressTriggers"]:
        parts.append("Stress triggers: " + " | ".join(profile["stressTriggers"]))

    return "\n".join(parts)


def decayMemories(db: Session, user_id: int):
    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .all()
    )

    now = datetime.now(timezone.utc)

    for memory in memories:
        if not memory.created_at:
            continue

        createdAt = memory.created_at

        if createdAt.tzinfo is None:
            createdAt = createdAt.replace(tzinfo=timezone.utc)

        ageDays = (now - createdAt).days

        if ageDays >= 7:
            memory.importance = max(1, memory.importance - 1)

        if ageDays >= 14:
            memory.importance = max(1, memory.importance - 1)

        if memory.importance <= 1 and ageDays > 10:
            db.delete(memory)

    db.commit()