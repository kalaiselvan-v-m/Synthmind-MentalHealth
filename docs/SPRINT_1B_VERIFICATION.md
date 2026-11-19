# Sprint 1B verification record

## Checks completed

- `python -m compileall -q backend` — passed.
- AST parse of every backend `.py` file — passed.
- Static scan confirms the old hard-coded PostgreSQL password and JWT placeholder are absent from the runtime database/auth configuration and `alembic.ini` — passed.
- Static scan confirms frontend source files no longer hard-code `http://127.0.0.1:8000` outside the central API client — passed.
- Static checks confirm Sprint 1A mood, memory, risk, recovery-plan and analytics routes use the authenticated current user's ID — passed.
- Required runtime dependency declarations (`alembic`, `python-jose`, `passlib`, `email-validator`, `bcrypt`) — present.
- `frontend/package.json` JSON parse — passed.
- `node --check frontend/src/api/api.js` — passed.

## Checks not completed

- Backend application import/runtime: not completed because this audit container does not have the PostgreSQL driver installed (`psycopg2`); it is declared in `backend/requirements.txt` as `psycopg2-binary`. This is an environment limitation, not evidence that the user's installed environment is broken.
- PostgreSQL connection, schema state, user registration/login integration, and data-isolation integration tests — not run.
- Frontend production build/lint — not run because `frontend/node_modules` is not present in the audit container.
- Ollama generation/streaming — not run because no local Ollama server/model is available in this audit container.
- Crisis-safety evaluation and clinical validation — not run and not claimed.

Static checks are useful but do not replace integration, security and user-acceptance testing on the target Windows machine.
