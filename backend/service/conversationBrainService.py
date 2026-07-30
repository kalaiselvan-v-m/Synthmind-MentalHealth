from backend.ml.conversationBrainPrediction import predictIntentML


SERIOUS_EMOTIONS = [
    "fear",
    "sadness",
    "grief",
    "nervousness",
    "remorse",
    "disappointment"
]

ANGRY_EMOTIONS = [
    "anger",
    "annoyance",
    "disapproval"
]

NEGATIVE_WORDS = [
    "sad",
    "tired",
    "exhausted",
    "lost",
    "lonely",
    "alone",
    "worthless",
    "failed",
    "failure",
    "scared",
    "anxious",
    "stress",
    "stressed",
    "overwhelmed",
    "drained",
    "empty",
    "hurt",
    "cry",
    "crying"
]

REASSURANCE_WORDS = [
    "nobody cares",
    "no one cares",
    "am i important",
    "not important",
    "you dont care",
    "you don't care",
    "you arent my friend",
    "you aren't my friend",
    "do you care",
    "i dont matter",
    "i don't matter"
]

RECOVERY_WORDS = [
    "better",
    "calm",
    "okay now",
    "fine now",
    "relieved",
    "peaceful",
    "good now",
    "feeling better"
]


def detectConversationStage(
    msg: str,
    emotion: str,
    wordCount: int,
    intent: str,
    risk: str
):
    negativeCount = sum(
        1 for word in NEGATIVE_WORDS
        if word in msg
    )

    hasReassuranceNeed = any(
        phrase in msg
        for phrase in REASSURANCE_WORDS
    )

    hasRecoverySignal = any(
        phrase in msg
        for phrase in RECOVERY_WORDS
    )

    if risk == "High":
        return "high_support_needed"

    if hasReassuranceNeed:
        return "reassurance_seeking"

    if hasRecoverySignal:
        return "recovering"

    if negativeCount >= 3:
        return "spiraling"

    if emotion in SERIOUS_EMOTIONS and wordCount >= 8:
        return "emotionally_deep"

    if emotion in SERIOUS_EMOTIONS:
        return "opening_up"

    if intent == "casual":
        return "casual_safe"

    return "stable"


def getStageInstructions(stage: str):
    instructions = {
        "high_support_needed": (
            "Be very calm, short, emotionally safe, and gently grounding. "
            "Do not overwhelm the user. Encourage reaching out to someone trusted if needed."
        ),

        "reassurance_seeking": (
            "Reassure first. Do not explain too much. "
            "Make the user feel emotionally held and not abandoned."
        ),

        "spiraling": (
            "Slow the conversation down. Use short grounded replies. "
            "Do not ask too many questions. Help the user feel steady."
        ),

        "emotionally_deep": (
            "Stay emotionally present. React naturally first, then gently continue. "
            "Avoid generic empathy phrases."
        ),

        "opening_up": (
            "Respond warmly and gently. Encourage the user without forcing depth."
        ),

        "recovering": (
            "Reflect the small improvement softly. Keep the tone hopeful but not overly excited."
        ),

        "casual_safe": (
            "Keep it relaxed, natural, and light. Do not over-support."
        ),

        "stable": (
            "Respond naturally and match the user's tone softly."
        )
    }

    return instructions.get(stage, instructions["stable"])


def analyzeConversation(message: str, emotion: str, risk: str = "Low"):
    msg = message.lower().strip()
    wordCount = len(msg.split())

    mlResult = predictIntentML(message)
    intent = mlResult["intent"]
    mlConfidence = mlResult["confidence"]

    # emotion correction
    if emotion in SERIOUS_EMOTIONS:
        intent = "emotional_support"

    if emotion in ANGRY_EMOTIONS and intent not in [
        "guidance",
        "style_request"
    ]:
        intent = "frustration"

    # short casual correction
    if wordCount <= 3 and intent not in [
        "emotional_support",
        "frustration"
    ]:
        if emotion not in SERIOUS_EMOTIONS:
            intent = "casual"

    # seriousness
    if intent == "emotional_support":
        seriousness = "serious"

    elif intent == "frustration":
        seriousness = "frustrated"

    else:
        seriousness = "light"

    # conversation stage
    conversationStage = detectConversationStage(
        msg=msg,
        emotion=emotion,
        wordCount=wordCount,
        intent=intent,
        risk=risk
    )

    stageInstruction = getStageInstructions(
        conversationStage
    )

    # tone
    if conversationStage == "reassurance_seeking":
        tone = "reassuring_grounded"

    elif conversationStage == "spiraling":
        tone = "slow_grounding"

    elif conversationStage == "emotionally_deep":
        tone = "emotionally_present"

    elif conversationStage == "opening_up":
        tone = "gentle_supportive"

    elif conversationStage == "recovering":
        tone = "soft_hopeful"

    elif intent == "emotional_support":
        tone = "calm_supportive"

    elif intent == "frustration":
        tone = "calm_grounded"

    elif intent == "casual":
        tone = "natural_casual"

    elif intent == "guidance":
        tone = "clear_guidance"

    elif intent == "style_request":
        tone = "style_adaptive"

    else:
        tone = "natural_friendly"

    # reply length
    if conversationStage in [
        "spiraling",
        "reassurance_seeking",
        "high_support_needed"
    ]:
        replyLength = "short"

    elif intent == "guidance":
        replyLength = "detailed"

    elif wordCount <= 5:
        replyLength = "short"

    else:
        replyLength = "matched"

    # memory usage
    useMemory = intent not in ["style_request"]

    if conversationStage in [
        "emotionally_deep",
        "reassurance_seeking",
        "spiraling"
    ]:
        useMemory = True

    # support level
    if risk == "High" and seriousness == "serious":
        supportLevel = "high_support"

    elif conversationStage in [
        "reassurance_seeking",
        "spiraling",
        "emotionally_deep"
    ]:
        supportLevel = "deep_support"

    elif seriousness == "serious":
        supportLevel = "gentle_support"

    else:
        supportLevel = "normal"

    return {
        "intent": intent,
        "mlConfidence": mlConfidence,
        "seriousness": seriousness,
        "tone": tone,
        "replyLength": replyLength,
        "useMemory": useMemory,
        "supportLevel": supportLevel,
        "conversationStage": conversationStage,
        "stageInstruction": stageInstruction
    }