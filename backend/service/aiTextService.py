"""Lazy-loaded text emotion model with a safe neutral fallback.

The API can start without the optional Transformers stack. The model is loaded
on first use rather than during FastAPI import/startup.
"""

MODEL_NAME = "wncelrcn/mindmap-deBERTa-goemotions-multilabel"
emotionPipeline = None
modelLoadAttempted = False

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
    "LABEL_27": "neutral",
}


def loadEmotionPipeline():
    global emotionPipeline, modelLoadAttempted
    if modelLoadAttempted:
        return emotionPipeline
    modelLoadAttempted = True
    try:
        from transformers import pipeline
        emotionPipeline = pipeline(
            "text-classification",
            model=MODEL_NAME,
            top_k=None,
        )
    except Exception as error:
        print("OPTIONAL EMOTION MODEL UNAVAILABLE:", str(error))
        emotionPipeline = None
    return emotionPipeline


def analyzeTextEmotion(text: str):
    model = loadEmotionPipeline()
    if model is None:
        return {
            "topEmotion": "neutral",
            "confidence": 0.0,
            "allEmotions": [],
        }

    try:
        results = model(text)[0]
        sortedResults = sorted(results, key=lambda item: item["score"], reverse=True)
        topEmotion = sortedResults[0]
        return {
            "topEmotion": label_map.get(topEmotion["label"], "unknown"),
            "confidence": round(float(topEmotion["score"]), 4),
            "allEmotions": [
                {
                    "emotion": label_map.get(item["label"], "unknown"),
                    "score": round(float(item["score"]), 4),
                }
                for item in sortedResults[:5]
            ],
        }
    except Exception as error:
        print("EMOTION MODEL ERROR:", str(error))
        return {"topEmotion": "neutral", "confidence": 0.0, "allEmotions": []}
