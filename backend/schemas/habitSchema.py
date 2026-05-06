from pydantic import BaseModel


class HabitCompleteRequest(BaseModel):
    habit_title: str
    habit_category: str = ""