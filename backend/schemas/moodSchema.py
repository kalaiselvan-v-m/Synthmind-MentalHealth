from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MoodCreate(BaseModel):
    mood: Literal["Happy", "Normal", "Low", "Overwhelmed"]
    note: str | None = Field(default=None, max_length=255)


class MoodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    mood: str
    note: str | None
    created_at: datetime
