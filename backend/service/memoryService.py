from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.models.userMemory import UserMemory
from backend.service.memoryLLMService import extractMemoryWithLLM


# -----------------------------------
# 🔥 FALLBACK MEMORY EXTRACTION
# -----------------------------------
def fallbackExtractMemory(message: str):
    msg = message.lower()

    memories = []

    # -----------------------------------
    # EXAM / STUDY
    # -----------------------------------
    if any(word in msg for word in ["exam", "test", "assignment", "deadline"]):
        memories.append({
            "type": "stress_trigger",
            "key": "academic_pressure",
            "value": "User often feels stressed about academic pressure.",
            "importance": 3
        })

    # -----------------------------------
    # INTERVIEW / CAREER
    # -----------------------------------
    if any(word in msg for word in ["interview", "placement", "job", "career"]):
        memories.append({
            "type": "stress_trigger",
            "key": "career_anxiety",
            "value": "User becomes nervous about career or interview situations.",
            "importance": 3
        })

    # -----------------------------------
    # ANXIETY
    # -----------------------------------
    if any(word in msg for word in ["anxiety", "anxious", "panic", "overthinking"]):
        memories.append({
            "type": "emotion_pattern",
            "key": "anxiety_pattern",
            "value": "User experiences anxiety or overthinking patterns.",
            "importance": 3
        })

    # -----------------------------------
    # FEAR
    # -----------------------------------
    if any(word in msg for word in ["scared", "fear", "afraid"]):
        memories.append({
            "type": "emotion_pattern",
            "key": "fear_pattern",
            "value": "User sometimes feels fearful or emotionally unsafe.",
            "importance": 3
        })

    # -----------------------------------
    # SLEEP
    # -----------------------------------
    if any(word in msg for word in ["sleep", "insomnia", "awake", "tired"]):
        memories.append({
            "type": "recurring_issue",
            "key": "sleep_issue",
            "value": "User may struggle with sleep or rest.",
            "importance": 2
        })

    # -----------------------------------
    # LONELINESS
    # -----------------------------------
    if any(word in msg for word in ["lonely", "alone", "isolated"]):
        memories.append({
            "type": "emotion_pattern",
            "key": "loneliness_pattern",
            "value": "User may experience loneliness sometimes.",
            "importance": 3
        })

    # -----------------------------------
    # MOTIVATION
    # -----------------------------------
    if any(word in msg for word in ["unmotivated", "motivation", "lazy", "burnout"]):
        memories.append({
            "type": "recurring_issue",
            "key": "motivation_issue",
            "value": "User struggles with motivation or burnout at times.",
            "importance": 2
        })

    # -----------------------------------
    # FAMILY PRESSURE
    # -----------------------------------
    if any(word in msg for word in ["family pressure", "parents", "expectation"]):
        memories.append({
            "type": "stress_trigger",
            "key": "family_pressure",
            "value": "Family expectations may emotionally affect the user.",
            "importance": 3
        })

    # -----------------------------------
    # SOCIAL ANXIETY
    # -----------------------------------
    if any(word in msg for word in ["social anxiety", "people judge", "awkward"]):
        memories.append({
            "type": "emotion_pattern",
            "key": "social_anxiety",
            "value": "User may feel socially anxious or judged.",
            "importance": 3
        })

    # -----------------------------------
    # CONFIDENCE
    # -----------------------------------
    if any(word in msg for word in ["confidence", "self doubt", "not good enough"]):
        memories.append({
            "type": "emotion_pattern",
            "key": "confidence_issue",
            "value": "User struggles with confidence or self-doubt.",
            "importance": 2
        })

    # -----------------------------------
    # COPING STRATEGIES
    # -----------------------------------
    if any(word in msg for word in ["music helps", "journaling helps", "walking helps"]):
        memories.append({
            "type": "coping_strategy",
            "key": "healthy_coping",
            "value": "User already has some healthy coping strategies.",
            "importance": 2
        })

    # -----------------------------------
    # TONE PREFERENCES
    # -----------------------------------
    if any(word in msg for word in ["bro", "homie", "talk casually", "friend"]):
        memories.append({
            "type": "preference",
            "key": "casual_tone",
            "value": "User prefers a casual friendly conversational tone.",
            "importance": 2
        })

    if any(word in msg for word in ["short replies", "reply short", "keep it short"]):
        memories.append({
            "type": "preference",
            "key": "short_reply_preference",
            "value": "User prefers shorter responses.",
            "importance": 2
        })
        
    # -----------------------------------
    # COMFORT / REASSURANCE PREFERENCE
    # -----------------------------------
    if any(word in msg for word in [
        "reassure me",
        "comfort me",
        "be comforting",
        "stay with me",
        "dont leave",
        "don't leave"
    ]):
        memories.append({
            "type": "preference",
            "key": "reassurance_preference",
            "value": (
                "User prefers emotionally reassuring and comforting responses."
            ),
            "importance": 3
        })

    # -----------------------------------
    # DISLIKES ROBOTIC STYLE
    # -----------------------------------
    if any(word in msg for word in [
        "dont sound robotic",
        "don't sound robotic",
        "talk naturally",
        "be real",
        "sound human",
        "talk like a person"
    ]):
        memories.append({
            "type": "preference",
            "key": "human_style_preference",
            "value": (
                "User prefers natural emotionally human conversation."
            ),
            "importance": 3
        })

    # -----------------------------------
    # FEWER QUESTIONS
    # -----------------------------------
    if any(word in msg for word in [
        "stop asking questions",
        "too many questions",
        "dont ask too much",
        "don't ask too much"
    ]):
        memories.append({
            "type": "preference",
            "key": "low_question_preference",
            "value": (
                "User prefers fewer reflective questions during support."
            ),
            "importance": 3
        })

    # -----------------------------------
    # MOTIVATIONAL STYLE
    # -----------------------------------
    if any(word in msg for word in [
        "motivate me",
        "push me",
        "encourage me"
    ]):
        memories.append({
            "type": "preference",
            "key": "motivation_preference",
            "value": (
                "User sometimes prefers motivating and encouraging responses."
            ),
            "importance": 2
        })

    # -----------------------------------
    # GROUNDING STYLE
    # -----------------------------------
    if any(word in msg for word in [
        "help me calm down",
        "ground me",
        "slow things down"
    ]):
        memories.append({
            "type": "preference",
            "key": "grounding_preference",
            "value": (
                "User responds well to grounding and calming emotional support."
            ),
            "importance": 3
        })

    return memories


# -----------------------------------
# 🔥 SAVE MEMORY
# -----------------------------------
def saveMemory(db: Session, user_id: int, memory: dict):

    if not memory.get("key") or not memory.get("value"):
        return None

    importance = memory.get("importance", 1)

    try:
        importance = int(importance)
    except Exception:
        importance = 1

    importance = max(1, min(importance, 5))

    existing = (
        db.query(UserMemory)
        .filter(
            UserMemory.user_id == user_id,
            UserMemory.memory_key == memory["key"]
        )
        .first()
    )

    # -----------------------------------
    # REINFORCE EXISTING MEMORY
    # -----------------------------------
    if existing:
        existing.memory_type = memory.get("type", existing.memory_type)
        existing.memory_value = memory["value"]

        existing.importance = min(
            5,
            max(existing.importance, importance) + 1
        )

        db.commit()
        db.refresh(existing)

        return existing

    # -----------------------------------
    # CREATE NEW MEMORY
    # -----------------------------------
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


# -----------------------------------
# 🔥 UPDATE LONG TERM MEMORY
# -----------------------------------
def updateLongTermMemory(db: Session, user_id: int, message: str):

    memories = []

    try:
        memories = extractMemoryWithLLM(message)
    except Exception as e:
        print("LLM memory extraction failed:", str(e))

    # fallback
    if not memories:
        memories = fallbackExtractMemory(message)

    savedMemories = []

    for memory in memories:
        saved = saveMemory(db, user_id, memory)

        if saved:
            savedMemories.append(saved)

    return savedMemories


# -----------------------------------
# 🔥 SMART MEMORY RETRIEVAL
# -----------------------------------
def getRelevantMemories(
    db: Session,
    user_id: int,
    message: str,
    limit: int = 6
):

    msg = message.lower()

    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .order_by(UserMemory.importance.desc())
        .all()
    )

    scored = []

    for memory in memories:

        score = memory.importance

        key = memory.memory_key.lower()
        value = memory.memory_value.lower()

        # -----------------------------------
        # TOPIC MATCHING
        # -----------------------------------
        if any(word in msg for word in ["exam", "test", "assignment"]):
            if "academic" in key or "exam" in value:
                score += 5

        if any(word in msg for word in ["interview", "placement", "career"]):
            if "career" in key or "interview" in value:
                score += 5

        if any(word in msg for word in ["anxiety", "panic", "overthinking"]):
            if "anxiety" in key:
                score += 4

        if any(word in msg for word in ["sleep", "tired"]):
            if "sleep" in key:
                score += 4

        if any(word in msg for word in ["alone", "lonely"]):
            if "loneliness" in key:
                score += 4

        # -----------------------------------
        # IMPORTANT MEMORY TYPES
        # -----------------------------------
        if memory.memory_type == "coping_strategy":
            score += 1

        if memory.memory_type == "stress_trigger":
            score += 2

        if memory.memory_type == "emotion_pattern":
            score += 2

        scored.append((score, memory))

    scored.sort(key=lambda x: x[0], reverse=True)

    finalMemories = []

    for score, memory in scored[:limit]:

        if memory.memory_key in ["short_key", "mention"]:
            continue

        if "clear human-readable memory" in memory.memory_value.lower():
            continue

        finalMemories.append(memory.memory_value)

    return " | ".join(finalMemories)


# -----------------------------------
# 🔥 PERSONALITY PROFILE
# -----------------------------------
def getPersonalityProfile(db: Session, user_id: int):

    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .order_by(UserMemory.importance.desc())
        .all()
    )

    grouped = {
        "preferences": [],
        "emotionalPatterns": [],
        "stressTriggers": [],
        "copingStrategies": [],
        "goals": []
    }

    for memory in memories:

        if memory.memory_type == "preference":
            grouped["preferences"].append(memory.memory_value)

        elif memory.memory_type == "emotion_pattern":
            grouped["emotionalPatterns"].append(memory.memory_value)

        elif memory.memory_type == "stress_trigger":
            grouped["stressTriggers"].append(memory.memory_value)

        elif memory.memory_type == "coping_strategy":
            grouped["copingStrategies"].append(memory.memory_value)

        elif memory.memory_type == "goal":
            grouped["goals"].append(memory.memory_value)

    return grouped


# -----------------------------------
# 🔥 FORMAT PERSONALITY PROFILE
# -----------------------------------
def formatPersonalityProfile(profile: dict):

    parts = []

    if profile["preferences"]:
        parts.append(
            "User preferences: " +
            " | ".join(profile["preferences"][:5])
        )

    if profile["emotionalPatterns"]:
        parts.append(
            "Emotional patterns: " +
            " | ".join(profile["emotionalPatterns"][:5])
        )

    if profile["stressTriggers"]:
        parts.append(
            "Stress triggers: " +
            " | ".join(profile["stressTriggers"][:5])
        )

    if profile["copingStrategies"]:
        parts.append(
            "Helpful coping methods: " +
            " | ".join(profile["copingStrategies"][:5])
        )

    if profile["goals"]:
        parts.append(
            "User goals: " +
            " | ".join(profile["goals"][:5])
        )

    return "\n".join(parts)


# -----------------------------------
# 🔥 MEMORY DECAY
# -----------------------------------
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

        # gradual decay
        if ageDays >= 10:
            memory.importance = max(1, memory.importance - 1)

        if ageDays >= 20:
            memory.importance = max(1, memory.importance - 1)

        # remove weak stale memories
        if memory.importance <= 1 and ageDays > 30:
            db.delete(memory)

    db.commit()