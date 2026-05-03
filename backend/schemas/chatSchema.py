from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    user_id: int
    message: str
    mode: Optional[str] = "guidance"


class ChatResponse(BaseModel):
    response: str


class ChatHistoryResponse(BaseModel):
    message: str
    response: str
    mode: str
    created_at: datetime

    class Config:
        orm_mode = True