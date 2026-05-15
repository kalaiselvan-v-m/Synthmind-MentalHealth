def detectCommunicationStyle(message: str):
    msg = message.lower()

    words = msg.split()

    casualWords = [
        "bro", "lol", "lmao", "bruh",
        "fr", "ngl", "wtf", "man"
    ]

    emotionalWords = [
        "feel", "lost", "worthless",
        "alone", "empty", "sad",
        "tired", "broken"
    ]

    humorWords = [
        "lol", "lmao", "😭", "😂"
    ]

    casualCount = sum(1 for word in casualWords if word in msg)
    emotionalCount = sum(1 for word in emotionalWords if word in msg)
    humorCount = sum(1 for word in humorWords if word in msg)

    # casual level
    if casualCount >= 2:
        casualLevel = "high"
    elif casualCount >= 1:
        casualLevel = "medium"
    else:
        casualLevel = "low"

    # emotional openness
    if emotionalCount >= 2:
        openness = "high"
    elif emotionalCount >= 1:
        openness = "medium"
    else:
        openness = "low"

    # humor
    if humorCount >= 2:
        humorStyle = "playful"
    elif humorCount >= 1:
        humorStyle = "light"
    else:
        humorStyle = "minimal"

    # energy
    if len(words) <= 3:
        messageEnergy = "low"
    elif len(words) <= 12:
        messageEnergy = "medium"
    else:
        messageEnergy = "high"

    return {
        "casualLevel": casualLevel,
        "humorStyle": humorStyle,
        "messageEnergy": messageEnergy,
        "openness": openness
    }