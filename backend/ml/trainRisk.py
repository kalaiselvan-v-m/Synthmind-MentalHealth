import pandas as pd
import lightgbm as lgb
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "riskData.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "risk.pkl")

df = pd.read_csv(DATA_PATH)

df["support_level"] = df["support_level"].map({
    "low": 0,
    "medium": 1,
    "high": 2
})

df["risk"] = df["risk"].map({
    "low": 0,
    "medium": 1,
    "high": 2
})

X = df[[
    "stress_score",
    "support_level",
    "low_mood_count",
    "negative_emotion_count"
]]

y = df["risk"]

model = lgb.LGBMClassifier(
    n_estimators=50,
    learning_rate=0.05,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, MODEL_PATH)

print("Risk model trained and saved successfully.")
print("Saved at:", MODEL_PATH)