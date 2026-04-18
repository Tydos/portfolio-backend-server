import os

from app import logger as _pkg_logger
from app.schemas.photo import Photo
from app.services.cloud_storage import CloudinaryUploader
from app.services.database import DatabaseManager

logger = _pkg_logger.getChild(__name__)


class PhotoUploadService:
    def __init__(self, uploader: CloudinaryUploader, database: DatabaseManager):
        self._uploader = uploader
        self._db = database

    def upload_one(self, filename: str, file_path: str, category: str, cloud_folder: str) -> int:
        result = self._uploader.upload(file_path, cloud_folder)
        photo = Photo(
            filename=filename,
            url=result["url"],
            width=result["width"],
            height=result["height"],
            category=category,
        )
        return self._db.upload_photo_to_db(photo)

    def upload_many(self, files: list[tuple[str, str]], category: str, cloud_folder: str) -> list[dict]:
        uploaded = []
        for fname, fpath in files:
            if self._db.filename_exists(fname.lower()):
                logger.info("Skipping duplicate: %s", fname)
                continue
            try:
                photo_id = self.upload_one(fname, fpath, category, cloud_folder)
                uploaded.append({"filename": fname, "id": photo_id})
            except Exception:
                logger.warning("Failed to upload %s, skipping", fname, exc_info=True)
        return uploaded
