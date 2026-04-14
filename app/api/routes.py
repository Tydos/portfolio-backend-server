"""API routes for portfolio data and photography management."""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.core.portfolio_data import projects, skills, data, photographs
from app.database.db import db
from app.schemas.photo import Photo

router = APIRouter()


@router.get("/api/data")
def get_data():
    """Get general portfolio data."""
    return JSONResponse(data)

@router.get("/api/projects")
def get_projects():
    """Get portfolio projects."""
    return JSONResponse(projects)

@router.get("/api/skills")
def get_skills():
    """Get skills list."""
    return JSONResponse(skills)

#fallback for when the supabase-db cannot be accessed
@router.get("/api/photographs")
def get_photographs():
    """Get all photographs."""
    return JSONResponse(photographs)

@router.get("/api/images")
def get_photos_from_db(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    """Fetch paginated photographs from database."""
    try:
        photos = db.fetch_photographs(limit, offset)
        if photos is None:
            raise HTTPException(status_code=500, detail="Failed to fetch photos from database")
        return photos
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#admin
@router.post("/upload", status_code=201)
def upload_photographs(photo: Photo):
    """Upload a new photograph to the database."""
    try:
        photo_id = db.upload_photo_to_db(photo)
        return {
            "message": "Photo uploaded successfully",
            "id": photo_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/fetch")
# def get_photos():
#     """Fetch photographs from local storage."""
#     try:
#         photos = fetch_local_photos()
#         if photos is None:
#             raise HTTPException(status_code=500, detail="Failed to fetch local photos")
#         return photos
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health():
    """Health check endpoint with database status."""
    records = db.view_records()
    if records is None:
        return {
            "message": "server active",
            "database": "connection failed"
        }
    return {
        "message": "server active",
        "database": "connected"
    }


@router.get("/")
def read_root():
    """Welcome message for the API gateway."""
    return JSONResponse({"message": "Portfolio Backend API Gateway"})
