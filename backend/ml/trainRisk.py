
import os
import joblib
import pandas as pd
import lightgbm as lgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "data", "riskData.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "ml", "risk.pkl"
)

FEATURES = [
    "stress_score",
    "support_level",
    "low_mood_count",
    "negative_emotion_count"
]

SUPPORT_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}

RISK_MAP = {
    "low": 0,
    "medium": 1,
    "high": 2
}


def main():

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    required = FEATURES + ["risk"]

    missing = [
        column for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df = df.dropna(subset=required).copy()

    df["support_level"] = (
        df["support_level"]
        .astype(str)
        .str.lower()
        .map(SUPPORT_MAP)
    )

    df["risk"] = (
        df["risk"]
        .astype(str)
        .str.lower()
        .map(RISK_MAP)
    )

    df = df.dropna(subset=FEATURES + ["risk"])

    class_counts = df["risk"].value_counts()

    print("\nTraining data class distribution:")
    print(class_counts)

    required_classes = {0, 1, 2}

    if set(class_counts.index) != required_classes:
        raise ValueError(
            "Training requires Low, Medium and High classes."
        )

    if class_counts.min() < 30:
        raise ValueError(
            "Insufficient training data. "
            "Collect at least 30 independently labelled "
            "records for EACH risk class before training. "
            "Do not duplicate records to meet this requirement."
        )

    X = df[FEATURES]
    y = df["risk"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        num_leaves=7,
        random_state=42,
        verbosity=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1, 2],
            target_names=["Low", "Medium", "High"],
            zero_division=0
        )
    )

    print("\nConfusion matrix:")
    print(confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1, 2]
    ))

    joblib.dump(model, MODEL_PATH)

    print("\nModel trained and saved successfully.")
    print("Model path:", MODEL_PATH)


if __name__ == "__main__":
    main()
