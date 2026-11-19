# Database migration warning — do not run `alembic upgrade head`

The current historical migration chain is not safe to apply as-is:

- `alembic/versions/ea0f4ab31ecd_add_habit_tracking.py` contains an `upgrade()` that drops `journal_entries`.
- `alembic/versions/b4f8f3c39c29_add_crisis_events.py` contains an `upgrade()` that drops both `journal_entries` and `habit_completions`.
- `alembic/versions/35bc1176d4aa_add_journal.py` is a no-op despite its name.
- `alembic/env.py` previously omitted several models from migration metadata; Sprint 1B now registers all models, but this does not repair the historical revision operations.

**Do not execute `alembic upgrade head` against a database containing user data.**

Before a migration repair is prepared, the actual database state must be established:

1. Is this database empty, or does it contain user data?
2. What does `alembic current` report?
3. Which tables currently exist, especially `journal_entries` and `habit_completions`?
4. Is there a verified backup that has been tested for restoration?

A safe repair for a database that has already applied a destructive revision differs from a repair for a fresh database. The historical revisions have intentionally not been rewritten in this patch because changing already-applied migration files can also create schema/version drift.

For local development, `AUTO_CREATE_TABLES=true` is supported as a convenience. SQLAlchemy `create_all()` creates missing tables but does not migrate or repair existing columns. It is not a production migration strategy. Set `AUTO_CREATE_TABLES=false` outside development.
