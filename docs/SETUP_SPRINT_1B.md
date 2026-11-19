# Local setup after Sprint 1B

## 1. Create backend environment settings

From the project root, copy `.env.example` to `.env`.

Edit `.env` and set:

- `DATABASE_URL` to your PostgreSQL username, password and database.
- `SECRET_KEY` to a random secret at least 32 characters long. Do not reuse the example placeholder.
- Keep `ENVIRONMENT=development` and `AUTO_CREATE_TABLES=true` only for local development.

A random secret can be generated with Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## 2. Install backend dependencies

Run from the project root (inside your activated virtual environment):

```bash
pip install -r backend/requirements.txt
```

The optional emotion and embedding models are listed separately. They are not required for the API to import and start:

```bash
pip install -r backend/requirements-ml.txt
```

That optional install is large and may take time. If it is not installed, emotion classification uses a neutral fallback and RAG embedding search is skipped.

## 3. Start Ollama

Install/start Ollama, then pull the model configured in `.env`:

```bash
ollama pull llama3.2:1b
```

If you use a different local model, update `OLLAMA_MODEL` in `.env`. Ollama must be running for chat/journal generation; the backend will return a safe fallback if it is unavailable.

## 4. Start the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

Check `http://127.0.0.1:8000/health` for the API health response.

## 5. Configure and start the frontend

Copy `frontend/.env.example` to `frontend/.env` if you need a non-default API address. Then:

```bash
cd frontend
npm install
npm run dev
```

## Important

Do not run `alembic upgrade head` until the historical migration warning has been resolved against the actual database state. See `DATABASE_MIGRATION_WARNING.md`.
