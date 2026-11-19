# Sprint 1B — configuration, startup and local AI hardening

This package is cumulative: it includes the Sprint 1A authentication/data-scope patch and the changes listed below.

## Backend changes

- `backend/config/settings.py`: loads project-root `.env`, validates the database URL and JWT secret, and centralizes CORS, token lifetime, table-creation and Ollama settings.
- `backend/config/security.py`: centralizes JWT settings.
- `backend/config/database.py`: removes the committed database password, uses environment configuration and enables connection health checks.
- `backend/models/__init__.py`: registers every SQLAlchemy model before development table creation and Alembic metadata inspection.
- `backend/main.py`: uses FastAPI lifespan, environment-based CORS, development-only `create_all`, and a health endpoint.
- `backend/service/authService.py`, `backend/dependencies/authDependency.py`, `backend/schemas/authSchema.py`, `backend/routes/authRoute.py`: validates passwords, normalizes email, handles duplicate-registration races, uses configured JWT secrets and returns consistent authentication errors.
- `backend/service/llmService.py`: replaces the mandatory Groq import with local Ollama HTTP calls; adds request timeouts and safe fallbacks.
- `backend/service/memoryLLMService.py`: shares Ollama settings and checks HTTP failures.
- `backend/service/aiTextService.py`: delays optional Transformers loading until first use and falls back safely if unavailable.
- `backend/service/ragMemoryService.py`: delays SentenceTransformers loading until embedding use and avoids failing chat requests when the optional model is unavailable.
- `alembic/env.py`: imports all models and reads the configured database URL.
- `alembic.ini`: removes the committed database credential.
- `backend/requirements.txt`: adds missing runtime dependencies; `backend/requirements-ml.txt` lists optional heavy ML dependencies separately.

## Frontend changes

- `frontend/src/api/api.js`: centralizes the configurable API base URL, request timeout and bearer-token attachment.
- `frontend/src/pages/Login.jsx` and `Register.jsx`: use the shared API client rather than hard-coded localhost fetch calls.
- Fetch-based screens now use `API_BASE_URL` rather than embedding the development server address.
- Chat UI text now says “Preview trusted contact message”; the current backend endpoint creates a preview and does not send an SMS or email.
- `.env.example` and `frontend/.env.example` document local configuration.

## Sprint 1A files carried forward

- `backend/routes/moodRoute.py`
- `backend/schemas/moodSchema.py`
- `backend/routes/memoryRoute.py`
- `backend/routes/riskRoute.py`
- `backend/routes/recoveryPlanRoute.py`
- `backend/routes/analyticsRoute.py`
- `frontend/src/api/api.js`
- `frontend/src/pages/Mood.jsx`
- `frontend/src/components/MoodPopup.jsx`
- `frontend/src/pages/RecoveryPlan.jsx`
- `frontend/src/pages/Insights.jsx`
- `docs/SPRINT_1A_CHANGELOG.md`

## Not claimed as complete

- No live PostgreSQL connection or data migration was run.
- No frontend npm build was run in this environment.
- No Ollama request was made; Ollama must be installed, running and have the configured model pulled.
- No clinical validation is claimed for crisis detection, risk scoring or emotion classification.
- Historical Alembic migrations remain unsafe; see `DATABASE_MIGRATION_WARNING.md`.
