"""API routes for portfolio data and photography management."""

import os
import tempfile

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from app import logger as _pkg_logger
from app.auth import verify_admin_key
from app.portfolio_data import projects, photographs
from app.services.database import db
from app.services.cloud_storage import CloudinaryUploader
from app.services.photo_upload import PhotoUploadService

router = APIRouter()
logger = _pkg_logger.getChild(__name__)

_uploader = CloudinaryUploader()
_upload_service = PhotoUploadService(_uploader, db)


@router.get("/api/projects")
def get_projects():
    return {"projects": projects}

@router.get("/api/images")
def get_images(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    # falls back to static data if DB is unavailable
    try:
        return db.fetch_photographs(limit, offset)
    except Exception:
        logger.exception("Database unavailable, falling back to static photographs")
        return photographs


@router.post("/api/upload", status_code=201, dependencies=[Depends(verify_admin_key)])
async def upload_photographs(
    file: UploadFile = File(...),
    category: str = Form(default="nature"),
    cloud_folder: str = Form(default="portfolio/images"),
):
    if not file.filename.lower().endswith((".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only .jpg/.jpeg files are accepted")

    suffix = os.path.splitext(file.filename)[1] or ".jpg"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        uploaded = _upload_service.upload_many([(file.filename, tmp_path)], category, cloud_folder)
    finally:
        if tmp_path:
            os.unlink(tmp_path)
    return {"uploaded": len(uploaded), "photos": uploaded}


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
