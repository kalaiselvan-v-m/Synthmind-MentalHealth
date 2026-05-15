def detectAttachmentSignal(message: str):
    msg = message.lower()

    phrases = [
        "you don't care",
        "you dont care",
        "you aren't my friend",
        "you arent my friend",
        "you are rude",
        "you sound rude",
        "you don't understand",
        "you dont understand",
        "nobody cares",
        "i am not important",
        "i'm not important",
        "i feel worthless",
        "i dont feel worthy",
        "i don't feel worthy",
    ]

    return any(phrase in msg for phrase in phrases)


def buildEmotionalFlow(recentEmotions, message: str):
    attachmentSignal = detectAttachmentSignal(message)

    negativeEmotions = ["sadness", "fear", "grief", "nervousness", "remorse", "disappointment"]

    negativeCount = sum(1 for emotion in recentEmotions if emotion in negativeEmotions)

    if attachmentSignal:
        emotionalState = "reassurance_seeking"

    elif negativeCount >= 3:
        emotionalState = "emotionally_heavy"

    elif negativeCount >= 1:
        emotionalState = "emotionally_sensitive"

    else:
        emotionalState = "stable_or_casual"

    return {
        "recentEmotions": recentEmotions,
        "attachmentSignal": attachmentSignal,
        "emotionalState": emotionalState
    }