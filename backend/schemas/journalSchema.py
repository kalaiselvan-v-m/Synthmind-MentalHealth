from pydantic import BaseModel


class CreateJournalRequest(BaseModel):
    content: str


class JournalResponse(BaseModel):
    id: int
    content: str
    emotion: str
    ai_summary: str
    created_at: str