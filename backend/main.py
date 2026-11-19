from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config.database import Base, SessionLocal, engine
from backend.config.settings import AUTO_CREATE_TABLES, CORS_ORIGINS, ENVIRONMENT

# Import every model before create_all so SQLAlchemy metadata is complete.
import backend.models  # noqa: F401

from backend.routes.analyticsRoute import router as analytics_router
from backend.routes.authRoute import router as auth_router
from backend.routes.chatRoute import router as chat_router
from backend.routes.crisisSupportRoute import router as crisis_support_router
from backend.routes.emotionalInsightRoute import router as emotional_insight_router
from backend.routes.habitSuggestionRoute import router as habit_router
from backend.routes.habitTrackingRoute import router as habit_tracking_router
from backend.routes.journalRoute import router as journal_router
from backend.routes.memoryRoute import router as memory_router
from backend.routes.moodRoute import router as mood_router
from backend.routes.onboardingRoute import router as onboarding_router
from backend.routes.profileRoute import router as profile_router
from backend.routes.recommendationRoute import router as recommendation_router
from backend.routes.recoveryIntelligenceRoute import router as recovery_intelligence_router
from backend.routes.recoveryPlanRoute import router as recovery_plan_router
from backend.routes.reminderRoute import router as reminder_router
from backend.routes.riskRoute import router as risk_router
from backend.routes.trustedContactRoute import router as trusted_contact_router
from backend.routes.weeklyReportRoute import router as weekly_report_router
from backend.utils.onboardingQuestion import seed_onboarding_questions

logger = logging.getLogger("synthmind")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if AUTO_CREATE_TABLES:
        if ENVIRONMENT != "development":
            raise RuntimeError(
                "AUTO_CREATE_TABLES is only allowed in development. "
                "Use reviewed database migrations in other environments."
            )
        Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_onboarding_questions(db)
    except Exception:
        db.rollback()
        logger.exception("Onboarding question seeding failed")
        if ENVIRONMENT != "development":
            raise
    finally:
        db.close()
    yield


app = FastAPI(title="SynthMind Backend", version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "synthmind-api"}


app.include_router(onboarding_router)
app.include_router(mood_router)
app.include_router(chat_router)
app.include_router(risk_router)
app.include_router(analytics_router)
app.include_router(recovery_plan_router)
app.include_router(recommendation_router)
app.include_router(memory_router)
app.include_router(auth_router)
app.include_router(weekly_report_router)
app.include_router(journal_router)
app.include_router(profile_router)
app.include_router(habit_router)
app.include_router(habit_tracking_router)
app.include_router(reminder_router)
app.include_router(emotional_insight_router)
app.include_router(trusted_contact_router)
app.include_router(recovery_intelligence_router)
app.include_router(crisis_support_router)
