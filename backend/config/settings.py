"""Environment-backed application settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Missing required environment variable {name}. "
            "Copy .env.example to .env and set the value."
        )
    return value


DATABASE_URL = _required("DATABASE_URL")
SECRET_KEY = _required("SECRET_KEY")
if len(SECRET_KEY) < 32 or "replace-this" in SECRET_KEY.lower():
    raise RuntimeError("SECRET_KEY must be a unique random value of at least 32 characters.")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").strip().lower()
AUTO_CREATE_TABLES = os.getenv(
    "AUTO_CREATE_TABLES", "true" if ENVIRONMENT == "development" else "false"
).strip().lower() in {"1", "true", "yes", "on"}
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat").strip()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b").strip()
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90"))
