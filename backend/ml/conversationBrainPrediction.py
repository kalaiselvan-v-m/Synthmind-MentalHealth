import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "conversationBrain.pkl")

model = None


def loadConversationBrainModel():
    global model

    if model is None:
        model = joblib.load(MODEL_PATH)

    return model


def predictIntentML(message: str):
    try:
        brainModel = loadConversationBrainModel()

        prediction = brainModel.predict([message])[0]

        probabilities = brainModel.predict_proba([message])[0]
        confidence = max(probabilities)

        return {
            "intent": prediction,
            "confidence": round(float(confidence), 4)
        }

    except Exception as e:
        print("CONVERSATION BRAIN ML ERROR:", str(e))

        return {
            "intent": "normal",
            "confidence": 0.0
        }