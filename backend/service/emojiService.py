emojiEmotionMap = {
    "😢": "sadness",
    "😭": "sadness",
    "😔": "sadness",
    "😞": "sadness",
    "😟": "fear",
    "😰": "nervousness",
    "😨": "fear",
    "😡": "anger",
    "😠": "anger",
    "😊": "joy",
    "😄": "joy",
    "😍": "love",
    "😴": "tired",
    "😵": "overwhelmed",
    "💔": "grief",
    "❤️": "love"
}


def detectEmojiEmotions(text: str):
    detected = []

    for emoji, emotion in emojiEmotionMap.items():
        if emoji in text:
            detected.append(emotion)

    return detected