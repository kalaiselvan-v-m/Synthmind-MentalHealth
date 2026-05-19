from sentence_transformers import SentenceTransformer
import numpy as np

from sqlalchemy.orm import Session

from backend.models.ragMemory import RagMemory


model = None


IMPORTANT_WORDS = [
    "stress", "stressed", "anxiety", "anxious", "fear", "scared",
    "sad", "alone", "lonely", "worthless", "failure", "failed",
    "interview", "exam", "placement", "career", "family", "friend",
    "relationship", "sleep", "tired", "exhausted", "overwhelmed",
    "hurt", "cry", "lost", "myself", "important", "nobody cares"
]


NEGATIVE_EMOTIONS = [
    "fear", "sadness", "grief", "nervousness",
    "remorse", "disappointment", "anger"
]


def loadEmbeddingModel():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def createEmbedding(text: str):
    embeddingModel = loadEmbeddingModel()
    vector = embeddingModel.encode(text)

    return vector.astype(float).tolist()


def cosineSimilarity(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def calculateImportance(text: str, emotion: str = "neutral"):
    msg = text.lower()
    score = 0.25

    if emotion in NEGATIVE_EMOTIONS:
        score += 0.25

    if any(word in msg for word in IMPORTANT_WORDS):
        score += 0.25

    if len(msg.split()) >= 12:
        score += 0.15

    if any(phrase in msg for phrase in [
        "i feel",
        "i am feeling",
        "i don't feel",
        "i dont feel",
        "i failed",
        "i can't",
        "i cant",
        "i need",
        "i'm scared",
        "im scared"
    ]):
        score += 0.2

    return min(score, 1.0)


def shouldSaveMemory(text: str, importance: float):
    if not text:
        return False

    clean = text.strip()

    if len(clean) < 10:
        return False

    casualMessages = [
        "hi", "hello", "hey", "yo", "ok", "okay",
        "hmm", "lol", "lmao", "fine", "good"
    ]

    if clean.lower() in casualMessages:
        return False

    return importance >= 0.35


def saveRagMemory(
    db: Session,
    user_id: int,
    text: str,
    emotion: str = "neutral"
):
    importance = calculateImportance(text, emotion)

    if not shouldSaveMemory(text, importance):
        return

    embedding = createEmbedding(text)

    memory = RagMemory(
        user_id=user_id,
        content=text,
        embedding=embedding,
        emotion=emotion,
        importance=importance
    )

    db.add(memory)
    db.commit()


def searchRagMemory(
    db: Session,
    user_id: int,
    query: str,
    emotion: str = "neutral",
    top_k: int = 4
):
    memories = (
        db.query(RagMemory)
        .filter(RagMemory.user_id == user_id)
        .order_by(RagMemory.importance.desc())
        .limit(100)
        .all()
    )

    if not memories:
        return ""

    queryEmbedding = createEmbedding(query)

    scored = []

    for memory in memories:
        if not memory.embedding:
            continue

        similarity = cosineSimilarity(
            queryEmbedding,
            memory.embedding
        )

        importanceScore = float(
            memory.importance or 0.3
        )

        emotionBonus = 0

        # emotional matching
        if emotion != "neutral":
            if memory.emotion == emotion:
                emotionBonus += 0.18

        # emotional category matching
        negativeCluster = [
            "fear",
            "sadness",
            "grief",
            "nervousness",
            "remorse",
            "disappointment"
        ]

        if (
            emotion in negativeCluster
            and memory.emotion in negativeCluster
        ):
            emotionBonus += 0.08

        # recent memories bonus
        recencyBonus = 0.05

        finalScore = (
            (similarity * 0.62)
            + (importanceScore * 0.23)
            + emotionBonus
            + recencyBonus
        )

        scored.append({
            "text": memory.content,
            "similarity": similarity,
            "importance": importanceScore,
            "emotionBonus": emotionBonus,
            "finalScore": finalScore
        })

    scored = sorted(
        scored,
        key=lambda x: x["finalScore"],
        reverse=True
    )

    best = [
        item["text"]
        for item in scored[:top_k]
        if item["finalScore"] > 0.42
    ]

    return "\n".join(best)