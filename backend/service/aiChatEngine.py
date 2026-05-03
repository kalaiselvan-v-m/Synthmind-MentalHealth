def generate_response(message: str, mode: str = "guidance"):
    msg = message.lower()

    # 🔹 Emotional detection
    if any(word in msg for word in ["sad", "lonely", "depressed", "tired"]):
        if mode == "vent":
            return "I'm here for you. Do you want to talk more about what's making you feel this way?"
        elif mode == "calm":
            return "Let's slow down. Take a deep breath… you're not alone."
        elif mode == "cbt":
            return "What thought is bothering you the most right now? Let's try to reframe it."
        else:
            return "That sounds really tough. I'm here to listen."

    if any(word in msg for word in ["stress", "exam", "pressure"]):
        return "It seems like you're feeling stressed. Try taking a short break or deep breathing."

    if any(word in msg for word in ["happy", "good", "great"]):
        return "That's amazing to hear! 😊 What made your day better?"

    if any(word in msg for word in ["alone", "no one", "empty"]):
        return "You may feel alone, but you're not. I'm here with you."

    # default
    return "I'm here to listen. Tell me more."