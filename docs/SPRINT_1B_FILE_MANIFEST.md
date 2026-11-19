# Sprint 1B file manifest

Compared with the newly uploaded `Synthmind-MentalHealth-demo.zip`: **39 existing files modified; 10 files added; 0 files removed.**

This is a cumulative package: it includes the prior Sprint 1A application changes plus the Sprint 1B changes. This manifest is the complete cumulative diff against the newly uploaded archive.

## Modified files
- `alembic.ini`
- `alembic/env.py`
- `backend/config/database.py`
- `backend/config/security.py`
- `backend/config/settings.py`
- `backend/dependencies/authDependency.py`
- `backend/main.py`
- `backend/models/__init__.py`
- `backend/requirements.txt`
- `backend/routes/analyticsRoute.py`
- `backend/routes/authRoute.py`
- `backend/routes/memoryRoute.py`
- `backend/routes/moodRoute.py`
- `backend/routes/recoveryPlanRoute.py`
- `backend/routes/riskRoute.py`
- `backend/schemas/authSchema.py`
- `backend/schemas/moodSchema.py`
- `backend/service/aiTextService.py`
- `backend/service/authService.py`
- `backend/service/llmService.py`
- `backend/service/memoryLLMService.py`
- `backend/service/ragMemoryService.py`
- `frontend/.gitignore`
- `frontend/src/App.jsx`
- `frontend/src/api/api.js`
- `frontend/src/components/EmotionalInsights.jsx`
- `frontend/src/components/MoodPopup.jsx`
- `frontend/src/pages/Chat.jsx`
- `frontend/src/pages/HabitTracker.jsx`
- `frontend/src/pages/Habits.jsx`
- `frontend/src/pages/Insights.jsx`
- `frontend/src/pages/Login.jsx`
- `frontend/src/pages/Mood.jsx`
- `frontend/src/pages/Onboarding.jsx`
- `frontend/src/pages/Profile.jsx`
- `frontend/src/pages/RecoveryPlan.jsx`
- `frontend/src/pages/Register.jsx`
- `frontend/src/pages/WeeklyReport.jsx`
- `frontend/src/pages/journal.jsx`

## Added files
- `.env.example`
- `backend/requirements-ml.txt`
- `docs/DATABASE_MIGRATION_WARNING.md`
- `docs/SETUP_SPRINT_1B.md`
- `docs/SPRINT_1A_CHANGELOG.md`
- `docs/SPRINT_1B_AUDIT_NOTES.md`
- `docs/SPRINT_1B_CHANGELOG.md`
- `docs/SPRINT_1B_FILE_MANIFEST.md`
- `docs/SPRINT_1B_VERIFICATION.md`
- `frontend/.env.example`

## Important interpretation

A file being listed as modified means its bytes differ from the newly uploaded archive. It does not mean every function in that file has been fully tested. See `SPRINT_1B_AUDIT_NOTES.md`, `SPRINT_1B_VERIFICATION.md` and `DATABASE_MIGRATION_WARNING.md` for remaining issues and verification limits.
