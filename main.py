from fastapi import FastAPI, HTTPException, Query
from data import projects, skills, data, photographs
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schema.Photo import Photo
from database import get_connection, upload_photo_to_db, fetch_photographs, view_records

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

#API route - upload images
@app.post("/upload")
def upload_photographs(photo:Photo):
    try:
        photo_id = upload_photo_to_db(photo)
        return {
            "message": "Photo uploaded successfully",
            "id": photo_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fetch")
def get_photos(
    limit: int = Query(),
    offset: int = Query()
):
    try:
        photos = fetch_photographs(limit, offset)
        return photos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {
        "message":"server active",
        "database": view_records()
    }

@app.get("/")
def read_root():
    return JSONResponse({"message": "Portfolio Backend API Gateway"})