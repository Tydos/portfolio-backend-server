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

**All routes** live in a single file: `app/api/routes.py`. Add new endpoints there using the existing `router` instance.

**Two data sources for portfolio content:**
1. **Static Python dicts** in `app/core/portfolio_data.py` — `data`, `skills`, `projects`, `photographs`. The `/api/data`, `/api/projects`, `/api/skills`, and `/api/photographs` routes serve these directly as JSON with no DB call.
2. **PostgreSQL** (`photographs` table) — accessed via `db` (a `DatabaseManager` singleton in `app/database/database.py`). The `/api/images` route queries this for paginated photo metadata.

**Database layer:** `DatabaseManager` in `app/database/database.py` uses `psycopg2.pool.ThreadedConnectionPool` (min=2, max=10). Always call `return_connection()` in a `finally` block. The pool is closed on app shutdown via the lifespan handler.

**Auth:** `app/utils/auth.py` — `verify_admin_key` FastAPI dependency that validates the `X-API-Key` header against `settings.ADMIN_API_KEY`.

**Schemas:** `app/schemas/photo.py` defines the `Photo` Pydantic model used for both the `POST /upload` request body and CSV-to-DB ingestion. The `category` field is a strict `Literal` enum.

**Logging:** `app/__init__.py` configures a module-level `logger` (plain `logging.Logger`) writing to `app/logs/app.log`. Child loggers in other modules use `logger.getChild(__name__)`.

**Image workflow:** Images are uploaded to Cloudinary via `app/utils/cloud_storage.py`, which generates `artifacts/image_metadata.csv`. That CSV is then ingested into PostgreSQL using `db.upload_images_from_csv()` (run `python app/database/database.py` directly to trigger this).

## Load Testing

```bash
# Requires wrk (brew install wrk on macOS)
bash app/tests/wrk_benchmark.sh
```

Results are written to `app/artifacts/wrk_results.txt`. Static routes sustain ~14,000–15,000 req/s; the DB-backed `/api/images` route is the bottleneck (~63 req/s).
