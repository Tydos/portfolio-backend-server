# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start with auto-reload (development)
python main.py
# or
uvicorn main:app --reload

# API docs available at http://localhost:8000/docs
```

## Environment Variables

Copy `.env.example` to `.env` and populate:
- `DATABASE_URL` — PostgreSQL connection string (Databricks-hosted)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- `ADMIN_API_KEY` — required for `POST /api/upload`

## Architecture

**Entry point:** `main.py` — creates the FastAPI app, attaches CORS middleware, includes the router, and manages the database pool lifecycle via `asynccontextmanager`.

**All routes** live in a single file: `app/routes.py`. Add new endpoints there using the existing `router` instance.

**Two data sources for portfolio content:**
1. **Static Python dicts** in `app/portfolio_data.py` — `projects`, `photographs`. The `/api/projects` route serves these directly as JSON with no DB call.
2. **PostgreSQL** (`photographs` table) — accessed via `db` (a `DatabaseManager` singleton in `app/database.py`). The `/api/images` route queries this for paginated photo metadata.

**Database layer:** `DatabaseManager` in `app/database.py` uses `psycopg2.pool.ThreadedConnectionPool` (min=2, max=10). Always call `return_connection()` in a `finally` block. The pool is closed on app shutdown via the lifespan handler.

**Auth:** `app/auth.py` — `verify_admin_key` FastAPI dependency that validates the `X-API-Key` header against `settings.ADMIN_API_KEY`.

**Schemas:** `app/photo.py` defines the `Photo` Pydantic model. The `category` field is a strict `Literal` enum.

**Logging:** `app/__init__.py` configures a module-level `logger` (plain `logging.Logger`) writing to stdout. Child loggers in other modules use `logger.getChild(__name__)`.

**Image workflow:** `POST /api/upload` accepts a `.jpg`/`.jpeg` file, uploads it to Cloudinary via `app/cloud_storage.py`, then persists metadata to PostgreSQL via `app/photo_upload.py` (PhotoUploadService). Duplicate filenames are skipped.

## Load Testing

```bash
# Requires wrk (brew install wrk on macOS)
bash app/wrk_benchmark.sh
```

Results are written to `app/wrk_results.txt`. Static routes sustain ~14,000–15,000 req/s; the DB-backed `/api/images` route is the bottleneck (~63 req/s).
