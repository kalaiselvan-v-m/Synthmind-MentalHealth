# SynthMind — Sprint 1A: Authenticated user data scope

## Scope
This patch keeps the existing SynthMind application and changes only the existing mood, memory, risk, recovery-plan, and analytics flows so user identity comes from the verified bearer token rather than a caller-supplied user ID.

## Changes

### Backend
- Mood check-ins now take `mood` and optional `note`; `user_id` is assigned from `getCurrentUser`.
- Mood history, summary, and calendar endpoints are scoped to the authenticated user.
- Memory listing and clearing are scoped to the authenticated user.
- Deleting one memory checks both the memory ID and authenticated owner; missing/non-owned memories return 404.
- Risk prediction and recovery-plan endpoints use the authenticated user.
- Analytics timeline uses the authenticated user.
- Mood input values are constrained to the four values currently used by the existing UI.
- Mood schema uses Pydantic v2 `ConfigDict(from_attributes=True)`.

### Frontend
- Axios now attaches the locally stored bearer token to API requests.
- Mood page, recovery plan, and insights page use the updated user-scoped endpoints.
- Mood check-in no longer sends a user ID or falls back to user ID `1`.
- Daily mood popup respects the existing `lastMoodDate` key instead of opening on every app mount.

## Verification
- `python -m compileall -q backend`: passed (syntax compilation only).
- Static scan: no remaining hardcoded `/mood/calendar/1`, `/recovery-plan/1`, `/analytics/timeline/`, or user-ID fallback in the modified frontend flows.
- Frontend production build: not verified. `npm ci` did not finish within the available execution window; Vite was therefore unavailable.
- Backend runtime/import tests: not verified. The uploaded requirements file does not list several packages imported by the application, including `python-jose`, `passlib`, and `groq`.
- No database migration or live database test was run.

## Important compatibility note
The following route contracts changed:
- `GET /mood/history/{user_id}` -> `GET /mood/history`
- `GET /mood/summary/{user_id}` -> `GET /mood/summary`
- `GET /mood/calendar/{user_id}` -> `GET /mood/calendar`
- `POST /mood/checkin` no longer accepts `user_id` in its JSON body
- `GET /risk/{user_id}` -> `GET /risk`
- `GET /recovery-plan/{user_id}` -> `GET /recovery-plan`
- `GET /analytics/timeline/{user_id}` -> `GET /analytics/timeline`
- Memory endpoints now use the authenticated user's scope instead of a supplied user ID.

Any external client or older frontend copy using the previous paths must be updated too.

## Next critical work (not changed in this patch)
1. Move the hardcoded PostgreSQL connection string and JWT secret into validated environment configuration.
2. Audit every mounted route for authentication and object-level authorization.
3. Reconcile Alembic history before running migrations: the uploaded migration chain includes `DROP TABLE` operations for `journal_entries` and `habit_completions`, while the initial migration does not create those tables. Do not run `alembic upgrade head` on a valuable database until its current schema and `alembic_version` are inspected and a safe migration plan is prepared.
4. Fix dependency manifest completeness and split runtime dependencies from development/ML tooling.
5. Replace direct Groq initialization with the selected LLM provider architecture only after tracing all callers and streaming response contracts.
6. Add automated tests for authentication, cross-user isolation, and existing frontend flows.

## Safety note
This is an engineering patch, not a clinical validation or production security certification. The risk score and crisis workflow require separate safety evaluation and human escalation design.
