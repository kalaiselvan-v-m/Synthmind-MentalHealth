from backend.ml.conversationBrainPrediction import predictIntentML


def analyzeConversation(message: str, emotion: str, risk: str = "Low"):
    msg = message.lower().strip()
    wordCount = len(msg.split())

    mlResult = predictIntentML(message)
    intent = mlResult["intent"]
    mlConfidence = mlResult["confidence"]

    seriousEmotions = [
        "fear", "sadness", "grief", "nervousness",
        "remorse", "disappointment"
    ]

    angryEmotions = ["anger", "annoyance", "disapproval"]

    # Emotion correction
    if emotion in seriousEmotions:
        intent = "emotional_support"

    if emotion in angryEmotions and intent not in ["guidance", "style_request"]:
        intent = "frustration"

    # Short casual correction
    if wordCount <= 3 and intent not in ["emotional_support", "frustration"]:
        if emotion not in seriousEmotions:
            intent = "casual"

    # seriousness
    if intent == "emotional_support":
        seriousness = "serious"
    elif intent == "frustration":
        seriousness = "frustrated"
    else:
        seriousness = "light"

    # tone
    if intent == "emotional_support":
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
    if intent == "guidance":
        replyLength = "detailed"
    elif wordCount <= 5:
        replyLength = "short"
    else:
        replyLength = "matched"

    # memory usage
    useMemory = intent not in ["casual", "style_request"]

    # support level
    if risk == "High" and seriousness == "serious":
        supportLevel = "high_support"
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
        "supportLevel": supportLevel
    }