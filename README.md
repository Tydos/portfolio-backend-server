

# Portfolio Backend Server
<img width="1349" height="310" alt="ChatGPT Image Feb 28, 2026 at 02_42_59 PM" src="https://github.com/user-attachments/assets/b38d744f-13c6-41a6-b573-fc1ca8b2c518" />

This backend is built using FastAPI and provides REST APIs to fetch portfolio data from local files and a PostgreSQL database hosted on Supabase, with images stored in Supabase Storage. Pydantic is used for schema validation.

---

## API Routes

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/` | — | API gateway welcome message |
| GET | `/api/images` | — | Paginated photographs from DB (`limit`, `offset` query params); falls back to static data if the DB is unavailable |
| POST | `/api/upload` | `X-API-Key` | Upload a single `.jpg`/`.jpeg` photo |
| POST | `/api/upload-batch` | `X-API-Key` | Upload many `.jpg`/`.jpeg` photos in one request |
| GET | `/api/health` | — | Health check (DB connectivity) |

---

## Image Upload Workflow

`POST /api/upload` handles the entire pipeline — Supabase Storage upload and DB persistence — in a single request. The image is stored in the bucket keyed by its filename, dimensions are read with Pillow, and the metadata row is written to PostgreSQL. If the filename already exists in the DB the uploaded object is rolled back and the request returns **409**.

```bash
curl -X POST http://localhost:8000/api/upload \
  -H "X-API-Key: <key>" \
  -F "file=@photo.jpg" \
  -F "category=nature"
```

Returns the created record:

```json
{ "id": 12, "filename": "photo.jpg", "url": "https://<project>.supabase.co/storage/v1/object/public/images/photo.jpg", "width": 800, "height": 600, "category": "nature" }
```

Single-upload form fields:

| Field | Default | Description |
|-------|---------|-------------|
| `file` | — | `.jpg`/`.jpeg` image file |
| `category` | `nature` | Photo category |

### Uploading a whole folder

`POST /api/upload-batch` takes a list of files (`files`) plus one shared `category` and processes them in a single request. A single bad file never aborts the batch — each file lands in `uploaded`, `skipped` (duplicate filename), or `failed` (wrong type / upload error).

```bash
curl -X POST http://localhost:8000/api/upload-batch \
  -H "X-API-Key: <key>" \
  -F "files=@a.jpg" -F "files=@b.jpg" -F "files=@c.jpg" \
  -F "category=nature"
```

```json
{
  "uploaded": [ { "id": 13, "filename": "a.jpg", "url": "...", "width": 800, "height": 600, "category": "nature" } ],
  "skipped":  [ { "filename": "b.jpg", "reason": "Duplicate filename: b.jpg" } ],
  "failed":   [ { "filename": "c.png", "error": "Only .jpg/.jpeg files are accepted" } ]
}
```

To upload an entire local folder, loop over it client-side (PowerShell):

```powershell
$curlArgs = @()
Get-ChildItem "C:\path\to\photos" -Recurse -File |
  Where-Object { $_.Extension -in '.jpg', '.jpeg' } |
  ForEach-Object { $curlArgs += '-F'; $curlArgs += "files=@$($_.FullName);type=image/jpeg" }
curl.exe -X POST http://localhost:8000/api/upload-batch `
  -H "X-API-Key: <key>" `
  @curlArgs `
  -F "category=nature"
```

---

## Database Schema

**Table: `photographs`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `filename` | VARCHAR | Filename of the image |
| `url` | VARCHAR | Public Supabase Storage URL |
| `category` | VARCHAR | Photo category (default `nature`) |
| `width` | INTEGER | Image width in pixels (default 1080) |
| `height` | INTEGER | Image height in pixels (default 1920) |
| `created_at` | TIMESTAMP | Row creation time (default `CURRENT_TIMESTAMP`) |

---

## Load Testing

Tested with `wrk` (8 threads, 100 connections, 15s). Static routes sustain ~14,000–15,000 req/s. The DB-backed `/api/images` route is the bottleneck at ~63 req/s due to connection pool overhead.

```bash
bash app/tests/wrk_benchmark.sh
# results written to app/tests/wrk_results.txt
```

---

## Project Structure

```
portfolio-backend-server/
├── main.py                      # Entry point — FastAPI app + lifespan
├── requirements.txt
├── app/
│   ├── __init__.py              # Logging configuration (stdout)
│   ├── auth.py                  # Admin API key dependency
│   ├── portfolio_data.py        # Static portfolio data (fallback)
│   ├── api/
│   │   └── routes.py            # All API endpoints
│   ├── schemas/
│   │   ├── config.py            # Settings (env vars)
│   │   └── photo.py             # Photo Pydantic model
│   ├── services/
│   │   ├── database.py          # DatabaseManager (psycopg2 pool)
│   │   ├── cloud_storage.py     # SupabaseUploader (+ legacy CloudinaryUploader)
│   │   └── photo_upload.py      # PhotoUploadService (upload + DB persist)
│   └── tests/
│       ├── test_api.py
│       ├── wrk_benchmark.sh
│       └── wrk_results.txt
```

---

## Running the Backend

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:
- `DATABASE_URL` — PostgreSQL connection string (Supabase)
- `ADMIN_API_KEY` — required for the upload endpoints
- `SUPABASE_URL`, `SUPABASE_KEY` — project URL and service-role key
- `SUPABASE_BUCKET` — existing **public** Storage bucket name (default `images`)

> Settings are read at import time via `load_dotenv(override=True)`, so changes to `.env` require restarting the server (uvicorn `--reload` watches `.py` files, not `.env`).

Start the server:
```bash
python main.py
# or
uvicorn main:app --reload
```

API docs at `http://localhost:8000/docs`

---

## Future Work

- Implement **pgvector** in PostgreSQL for image embedding and semantic search.
- Support **automatic image downscaling** before upload.
