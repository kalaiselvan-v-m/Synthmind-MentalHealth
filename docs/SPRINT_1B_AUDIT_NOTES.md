# Code audit notes and remaining work

The following are confirmed by static inspection of the supplied source. They are not all changed in Sprint 1B.

## Addressed in Sprint 1B

- Hard-coded PostgreSQL credentials removed from Python and Alembic configuration.
- Hard-coded JWT placeholder removed; application requires a configured secret.
- JWT bearer dependency now rejects missing/invalid credentials consistently.
- Registration/login input validation and email normalization improved.
- Core mood, memory, risk, recovery-plan and analytics routes retain Sprint 1A ownership scoping.
- Frontend API base URL is environment-configurable.
- Login/register use the shared API client.
- Groq is no longer imported; chat and journal generation use configured local Ollama.
- Optional Transformers and SentenceTransformers dependencies are no longer loaded at API import time.
- Model metadata registration is complete before development table creation/Alembic inspection.

## Still needs a separate, tested sprint

1. **Historical database migrations:** destructive and incomplete revisions described in `DATABASE_MIGRATION_WARNING.md`.
2. **Crisis safety:** current detection is phrase-based. It can miss indirect/ambiguous disclosures and can flag quoted or negated phrases. It is not clinically validated and must not be presented as diagnosis or dependable emergency triage.
3. **Trusted-contact notification:** `/trusted-contact/notify-preview` only returns a preview and logs an action. It does not send SMS/email. A real notification workflow needs consent, provider integration, delivery status, abuse prevention and tests.
4. **Account/data deletion:** profile endpoints clear chat and journal data, but there is no complete account deletion/export workflow covering all user-linked tables (moods, onboarding, memories, RAG memories, crisis events/actions, trusted contacts and habit records).
5. **Database integrity:** several user-owned tables use integer `user_id` columns without foreign keys; uniqueness/index constraints and cascade policy need a migration plan.
6. **Authentication hardening:** tokens are stored in browser `localStorage`; this remains exposed to same-origin script/XSS compromise. Rate limiting, login throttling, password reset, refresh/revocation and security headers are not implemented here.
7. **Privacy and retention:** chat, journal and crisis content is sensitive. Retention periods, user consent, data minimization, access audit and deletion semantics need product/legal review before real student deployment.
8. **Clinical and model validation:** risk scoring, emotion classification and support escalation need documented datasets, evaluation metrics, bias checks, human review and explicit non-diagnostic product language.
9. **Automated tests:** the repository does not currently provide a meaningful automated test suite for auth, cross-user access, crisis pathways, migrations or frontend flows.
10. **Frontend quality:** direct `fetch` calls still exist, although their base URL is now configurable and authenticated screens retain bearer headers. A follow-up can consolidate them into one request client and add consistent error handling.
11. **Deployment readiness:** HTTPS, production secrets, database backups, monitoring, structured logs, request limits, background jobs and deployment configuration remain to be implemented and verified.

## Verification status

This audit is based on source inspection and static checks. It does not establish that the app works against a live PostgreSQL database, that Ollama is reachable, or that all frontend routes build and behave correctly.
