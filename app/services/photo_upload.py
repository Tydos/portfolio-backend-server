from app import logger as _pkg_logger
from app.schemas.photo import Photo
from app.services.cloud_storage import SupabaseUploader
from app.services.database import DatabaseManager

logger = _pkg_logger.getChild(__name__)


class PhotoUploadService:
    def __init__(self, uploader: SupabaseUploader, database: DatabaseManager):
        self._uploader = uploader
        self._db = database

    def upload_one(self, file_bytes: bytes, filename: str, category: str) -> dict:
        result = self._uploader.upload(file_bytes, filename)
        photo = Photo(
            filename=filename,
            url=result["url"],
            width=result["width"],
            height=result["height"],
            category=category,
        )
        try:
            photo_id = self._db.upload_photo_to_db(photo)
        except Exception:
            self._uploader.delete(result["storage_key"])
            raise
        if photo_id is None:
            self._uploader.delete(result["storage_key"])
            raise ValueError(f"Duplicate filename: {filename}")
        return {
            "id": photo_id,
            "filename": filename,
            "url": result["url"],
            "width": result["width"],
            "height": result["height"],
            "category": category,
        }
