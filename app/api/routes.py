"""API routes for portfolio data and photography management."""

from fastapi import APIRouter, Depends, HTTPException, Query

from app import logger as _pkg_logger
from app.utils.auth import verify_admin_key
from app.core.portfolio_data import data, projects, skills, photographs
from app.database.database import db
from app.schemas.photo import Photo

router = APIRouter()
logger = _pkg_logger.getChild(__name__)

_PORTFOLIO_RESPONSE = {**data, "skills": skills, "projects": projects}


@router.get("/api/portfolio")
def get_portfolio():
    return _PORTFOLIO_RESPONSE


@router.get("/api/images")
def get_images(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    # falls back to static data if DB is unavailable
    try:
        return db.fetch_photographs(limit, offset)
    except Exception:
        logger.exception("Database unavailable, falling back to static photographs")
        return photographs


@router.post("/api/upload", status_code=201, dependencies=[Depends(verify_admin_key)])
def upload_photographs(photo: Photo):
    try:
        photo_id = db.upload_photo_to_db(photo)
        return {"message": "Photo uploaded successfully", "id": photo_id}
    except Exception:
        logger.exception("Failed to upload photo")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/health")
def health():
    if not db.ping():
        raise HTTPException(
            status_code=503,
            detail={"message": "server active", "database": "connection failed"}
        )
    return {"message": "server active", "database": "connected"}


@router.get("/")
def read_root():
    return {"message": "Portfolio Backend API Gateway"}
