from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config.database import Base, engine, SessionLocal

from backend.routes.onboardingRoute import router as onboarding_router
from backend.routes.moodRoute import router as mood_router
from backend.routes.chatRoute import router as chat_router
from backend.routes.riskRoute import router as risk_router
from backend.routes.analyticsRoute import router as analytics_router
from backend.routes.recoveryPlanRoute import router as recovery_plan_router
from backend.routes.recommendationRoute import router as recommendation_router
from backend.routes.memoryRoute import router as memory_router
from backend.routes.authRoute import router as auth_router
from backend.routes.weeklyReportRoute import router as weekly_report_router
from backend.routes.journalRoute import router as journal_router
from backend.routes.moodCalendarRoute import router as mood_calendar_router
from backend.routes.profileRoute import router as profile_router
from backend.routes.habitSuggestionRoute import router as habit_router
from backend.routes.habitTrackingRoute import router as habit_tracking_router
from backend.routes.reminderRoute import router as reminder_router

from backend.models import userMemory
from backend.models import onboarding
from backend.models import user
from backend.models import habit
from backend.utils.onboardingQuestion import seed_onboarding_questions

# ✅ CREATE APP ONLY ONCE
app = FastAPI(title="SynthMind Backend")

# ✅ ADD CORS HERE (after app creation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

# ✅ STARTUP EVENT
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_onboarding_questions(db)
    finally:
        db.close()

# ✅ ROUTES
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
app.include_router(mood_calendar_router)
app.include_router(profile_router)
app.include_router(habit_router)
app.include_router(habit_tracking_router)
app.include_router(reminder_router)
