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
- `DATABASE_URL` — PostgreSQL connection string (Supabase-hosted Postgres pooler)
- `ADMIN_API_KEY` — required for `POST /api/upload` (checked against the `X-API-Key` header)
- `SUPABASE_URL`, `SUPABASE_KEY` — Supabase project URL and service-role key (used by the default uploader)
- `SUPABASE_BUCKET` — Supabase Storage bucket name (default: `images`). Must be an existing **public** bucket, or uploads 404 with `Bucket not found`.
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` — legacy; only used by the unused `CloudinaryUploader`
- `LOG_LEVEL` — optional, defaults to `INFO`

Note: `app/schemas/config.py` calls `load_dotenv(override=True)` and reads env vars **at import time**, so changes to `.env` require a process restart — uvicorn's `--reload` watches `.py` files, not `.env`.

## Architecture

**Entry point:** `main.py` — creates the FastAPI app, attaches CORS middleware, includes the router, and closes the database pool on shutdown via an `asynccontextmanager` lifespan handler.

**All routes** live in `app/api/routes.py`. Add new endpoints there using the existing `router` instance. Active routes: `GET /`, `GET /api/images`, `POST /api/upload`, `POST /api/upload-batch`, `GET /api/health`. (`GET /api/projects` exists only as commented-out code.)

**Two data sources for portfolio content:**
1. **Static Python data** in `app/portfolio_data.py` — `projects`, `photographs`. Used as the fallback when the DB is unavailable.
2. **PostgreSQL** (`photographs` table) — accessed via `db` (a `DatabaseManager` singleton in `app/services/database.py`). `GET /api/images` queries this for paginated photo metadata and falls back to the static `photographs` on any DB error.

**Database layer:** `DatabaseManager` in `app/services/database.py` uses `psycopg2.pool.ThreadedConnectionPool` (min=2, max=10). Connections are borrowed/returned through the `_connection()` context manager. The pool is created lazily and closed on app shutdown via the lifespan handler. The `photographs` table columns: `id`, `filename`, `url`, `category` (default `nature`), `width` (default 1080), `height` (default 1920), `created_at`.

**Auth:** `app/auth.py` — `verify_admin_key` FastAPI dependency that validates the `X-API-Key` header against `settings.ADMIN_API_KEY`, raising 401 on mismatch.

**Schemas:** `app/schemas/photo.py` defines the `Photo` Pydantic model. `category` is a strict `Literal` enum and `filename` is validated to reject path-traversal characters. Settings/config live in `app/schemas/config.py`.

**Logging:** `app/__init__.py` defines `configure_logging()` (called on import), which attaches a stdout `StreamHandler` to the root logger at `LOG_LEVEL` (default `INFO`) so serverless platforms like Vercel collect runtime logs. Modules log via `logging.getLogger("app").getChild(__name__)`.

**Image workflow:** `POST /api/upload` accepts a single `.jpg`/`.jpeg` file plus a `category` form field. `SupabaseUploader` in `app/services/cloud_storage.py` reads the image dimensions via Pillow and `POST`s the bytes to Supabase Storage, keyed by the bare filename at the bucket root. `PhotoUploadService` in `app/services/photo_upload.py` then persists the metadata row to PostgreSQL; if the DB insert fails or the filename is a duplicate, the just-uploaded object is deleted and the request returns 409. `POST /api/upload-batch` accepts a list of files (`files`) plus one shared `category` and loops over `upload_one`, returning a `{"uploaded": [...], "skipped": [...], "failed": [...]}` summary — a single bad file never aborts the batch. `CloudinaryUploader` remains in the same file as a legacy alternative. Both uploaders expose the same duck-typed interface (`upload(file_bytes, filename) -> dict`, `delete(storage_key) -> bool`), so swapping them only requires changing the wiring in `routes.py`.

## Load Testing

```bash
# Requires wrk (brew install wrk on macOS)
bash app/tests/wrk_benchmark.sh
```

Results are written to `app/tests/wrk_results.txt`. Static routes sustain ~14,000–15,000 req/s; the DB-backed `/api/images` route is the bottleneck (~63 req/s).
