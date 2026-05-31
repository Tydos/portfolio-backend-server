"""API routes for portfolio data and photography management."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from app import logger as _pkg_logger
from app.auth import verify_admin_key
from app.portfolio_data import photographs
from app.services.database import db


from app.services.cloud_storage import CloudinaryUploader, SupabaseUploader
from app.services.photo_upload import PhotoUploadService

router = APIRouter()
logger = _pkg_logger.getChild(__name__)

_uploader = SupabaseUploader()
_upload_service = PhotoUploadService(_uploader, db)

# @router.get("/api/projects")
# def get_projects():
#     return {"projects": projects}

@router.get("/api/images")
def get_images(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    # falls back to static data if DB is unavailable
    try:
        return db.fetch_photographs(limit, offset)
    except Exception:
        logger.exception("Database unavailable, falling back to static photographs")
        return photographs


@router.post("/api/upload", status_code=201, dependencies=[Depends(verify_admin_key)])
async def upload(
    file: UploadFile = File(...),
    category: str = Form(default="nature"),
):
    if not file.filename.lower().endswith((".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only .jpg/.jpeg files are accepted")

    file_bytes = await file.read()
    try:
        photo = _upload_service.upload_one(file_bytes, file.filename, category)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return photo


@router.post("/api/upload-batch", dependencies=[Depends(verify_admin_key)])
async def upload_batch(
    files: list[UploadFile] = File(...),
    category: str = Form(default="nature"),
):
    """Upload many photos in one request. Returns a per-file summary; one bad
    file never aborts the batch."""
    results = {"uploaded": [], "skipped": [], "failed": []}
    for file in files:
        if not file.filename.lower().endswith((".jpg", ".jpeg")):
            results["failed"].append(
                {"filename": file.filename, "error": "Only .jpg/.jpeg files are accepted"}
            )
            continue
        try:
            file_bytes = await file.read()
            photo = _upload_service.upload_one(file_bytes, file.filename, category)
            results["uploaded"].append(photo)
        except ValueError as e:
            results["skipped"].append({"filename": file.filename, "reason": str(e)})
        except Exception as e:
            logger.exception("Failed to upload %s", file.filename)
            results["failed"].append({"filename": file.filename, "error": str(e)})
    return results


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
