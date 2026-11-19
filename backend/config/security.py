"""Central security configuration."""

from backend.config.settings import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    SECRET_KEY,
)

__all__ = ["ACCESS_TOKEN_EXPIRE_MINUTES", "JWT_ALGORITHM", "SECRET_KEY"]
