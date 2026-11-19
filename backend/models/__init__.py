"""Import every SQLAlchemy model so metadata is complete."""

from backend.models.chat import ChatHistory
from backend.models.crisisEvent import CrisisEvent
from backend.models.crisisSupportAction import CrisisSupportAction
from backend.models.habit import HabitCompletion
from backend.models.journal import JournalEntry
from backend.models.mood import Mood
from backend.models.onboarding import OnboardingQuestion, OnboardingResponse, UserMentalProfile
from backend.models.ragMemory import RagMemory
from backend.models.trustedContact import TrustedContact
from backend.models.user import User
from backend.models.userMemory import UserMemory

__all__ = [
    "ChatHistory",
    "CrisisEvent",
    "CrisisSupportAction",
    "HabitCompletion",
    "JournalEntry",
    "Mood",
    "OnboardingQuestion",
    "OnboardingResponse",
    "RagMemory",
    "TrustedContact",
    "User",
    "UserMemory",
    "UserMentalProfile",
]
