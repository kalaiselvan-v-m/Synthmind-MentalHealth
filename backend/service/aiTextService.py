from transformers import pipeline

MODEL_NAME = "wncelrcn/mindmap-deBERTa-goemotions-multilabel"

# 🔥 Load model ONCE (important for performance)
emotionPipeline = pipeline(
    "text-classification",
    model=MODEL_NAME,
    top_k=None
)

# 🔥 Label → Emotion mapping
label_map = {
    "LABEL_0": "admiration",
    "LABEL_1": "amusement",
    "LABEL_2": "anger",
    "LABEL_3": "annoyance",
    "LABEL_4": "approval",
    "LABEL_5": "caring",
    "LABEL_6": "confusion",
    "LABEL_7": "curiosity",
    "LABEL_8": "desire",
    "LABEL_9": "disappointment",
    "LABEL_10": "disapproval",
    "LABEL_11": "disgust",
    "LABEL_12": "embarrassment",
    "LABEL_13": "excitement",
    "LABEL_14": "fear",
    "LABEL_15": "gratitude",
    "LABEL_16": "grief",
    "LABEL_17": "joy",
    "LABEL_18": "love",
    "LABEL_19": "nervousness",
    "LABEL_20": "optimism",
    "LABEL_21": "pride",
    "LABEL_22": "realization",
    "LABEL_23": "relief",
    "LABEL_24": "remorse",
    "LABEL_25": "sadness",
    "LABEL_26": "surprise",
    "LABEL_27": "neutral"
}


def analyzeTextEmotion(text: str):
    try:
        results = emotionPipeline(text)[0]

        # Sort by confidence
        sortedResults = sorted(
            results,
            key=lambda item: item["score"],
            reverse=True
        )

        topEmotion = sortedResults[0]

        # Convert LABEL → actual emotion
        emotion_label = topEmotion["label"]
        emotion_name = label_map.get(emotion_label, "unknown")

        # Convert top 5 emotions
        top_emotions = []
        for item in sortedResults[:5]:
            label = item["label"]
            top_emotions.append({
                "emotion": label_map.get(label, "unknown"),
                "score": round(item["score"], 4)
            })

        return {
            "topEmotion": emotion_name,
            "confidence": round(topEmotion["score"], 4),
            "allEmotions": top_emotions
        }

    except Exception as e:
        print("EMOTION MODEL ERROR:", str(e))

        return {
            "topEmotion": "neutral",
            "confidence": 0.0,
            "allEmotions": []
        }