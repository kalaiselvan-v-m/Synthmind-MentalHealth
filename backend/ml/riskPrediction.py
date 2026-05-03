import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "risk.pkl")

model = None


def loadRiskModel():
    global model

    if model is None:
        model = joblib.load(MODEL_PATH)

    return model


def predictRiskML(stress_score, support_level, low_mood_count, negative_emotion_count):
    riskModel = loadRiskModel()

    support_map = {
        "low": 0,
        "medium": 1,
        "high": 2,
        "Low support system": 0,
        "Moderate support system": 1,
        "Good support system": 2
    }

    support_value = support_map.get(support_level, 1)

    X = np.array([[
        stress_score,
        support_value,
        low_mood_count,
        negative_emotion_count
    ]])

    prediction = riskModel.predict(X)[0]

    label_map = {
        0: "Low",
        1: "Medium",
        2: "High"
    }

    return label_map.get(int(prediction), "Low")