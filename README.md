

# Portfolio Backend Server
<img width="1349" height="310" alt="ChatGPT Image Feb 28, 2026 at 02_42_59 PM" src="https://github.com/user-attachments/assets/b38d744f-13c6-41a6-b573-fc1ca8b2c518" />

This backend is built using FastAPI and provides REST APIs to fetch portfolio data from local files and a PostgreSQL cloud database hosted on Databricks with images stored on Cloudinary. Pydantic is used for schema validation.

---

## API Routes

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/` | — | API gateway welcome message |
| GET | `/api/projects` | — | List of portfolio projects |
| GET | `/api/images` | — | Paginated photographs from DB (`limit`, `offset` query params) |
| GET | `/api/health` | — | Health check (DB connectivity) |
| POST | `/api/upload` | `X-API-Key` | Upload a single `.jpg`/`.jpeg` photo |

---

## Image Upload Workflow

`POST /api/upload` handles the entire pipeline — Cloudinary upload and DB persistence — in a single request.

```bash
curl -X POST http://localhost:8000/api/upload \
  -H "X-API-Key: <key>" \
  -F "file=@photo.jpg" \
  -F "category=nature"
```

Returns `{"uploaded": N, "photos": [{"filename": "...", "id": ...}]}`. Skips the file if the filename already exists in the DB.

Form fields:
| Field | Default | Description |
|-------|---------|-------------|
| `file` | — | `.jpg`/`.jpeg` image file |
| `category` | `nature` | Photo category |
| `cloud_folder` | `portfolio/images` | Cloudinary destination folder |

---

## Database Schema

**Table: `photographs`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL | Primary key |
| `filename` | VARCHAR | Filename of the image |
| `url` | TEXT | Cloudinary URL |
| `width` | INTEGER | Image width in pixels (default 1080) |
| `height` | INTEGER | Image height in pixels (default 1920) |
| `category` | VARCHAR | Photo category (default `nature`) |

---

## Load Testing

Tested with `wrk` (8 threads, 100 connections, 15s). Static routes sustain ~14,000–15,000 req/s. The DB-backed `/api/images` route is the bottleneck at ~63 req/s due to connection pool overhead.

```bash
bash app/tests/wrk_benchmark.sh
# results written to app/artifacts/wrk_results.txt
```

---

## Project Structure

```
portfolio-backend-server/
├── main.py                    # Entry point — FastAPI app + lifespan
├── requirements.txt
├── app/
│   ├── api/
│   │   └── routes.py          # All API endpoints
│   ├── core/
│   │   ├── config.py          # Settings (env vars)
│   │   └── portfolio_data.py  # Static portfolio data
│   ├── database/
│   │   └── database.py        # DatabaseManager (psycopg2 pool)
│   ├── schemas/
│   │   └── photo.py           # Photo Pydantic model
│   ├── utils/
│   │   ├── auth.py            # Admin API key dependency
│   │   └── cloud_storage.py   # CloudinaryUploader
│   ├── tests/
│   │   ├── test_api.py
│   │   └── wrk_benchmark.sh
│   └── artifacts/
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
- `DATABASE_URL` — PostgreSQL connection string
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- `ADMIN_API_KEY` — required for `POST /api/upload`

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
- Support **automatic image downscaling** before Cloudinary upload.
