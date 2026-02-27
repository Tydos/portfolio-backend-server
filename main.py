from fastapi import FastAPI, HTTPException, Query
from data import projects, skills, data, photographs
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schema.Photo import Photo
from db import get_connection

app = FastAPI(
    title="Portfolio Backend Server",
    description="Vercel + FastAPI API Gateway for Portfolio",
    version="1.0.0",
)

#Allow everyone to access the backend online
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, etc.
    allow_headers=["*"],     # allow all headers
)

#static API routes for populating data
@app.get("/api/data")
def get_data():
    return JSONResponse(data)

@app.get("/api/projects")
def get_projects():
    return JSONResponse(projects)

@app.get("/api/skills")
def get_skills():
    return JSONResponse(skills)

@app.get("/api/photographs")
def get_photographs():
    return JSONResponse(photographs)

#CRUD API route for photo blog
@app.post("/uploadphotos")
def upload_photographs(photo:Photo):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO photographs (title, url)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (photo.title, photo.url)
                )
                photo_id = cur.fetchone()[0]
                conn.commit()

        return {
            "message": "Photo uploaded successfully",
            "id": photo_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getphotographs")
def get_photos(
    limit: int = Query(),
    offset: int = Query()
):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, title, url, category, description
                    FROM photographs
                    ORDER BY id
                    LIMIT %s OFFSET %s;
                    """,
                    (limit, offset)
                )
                rows = cur.fetchall()

        return [
            {"id": r[0], "title": r[1], "url": r[2], "category": r[3], "description": r[4]}
            for r in rows
        ]

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return JSONResponse({"message": "Portfolio Backend API Gateway"})