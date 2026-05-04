import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "conversationIntentData.csv")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "conversationBrain.pkl")

df = pd.read_csv(DATA_PATH)

X = df["text"]
y = df["intent"]

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X, y)

joblib.dump(model, MODEL_PATH)

print("Conversation brain model trained successfully.")
print("Saved at:", MODEL_PATH)