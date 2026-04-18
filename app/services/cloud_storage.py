# Cloudinary configuration and upload operations.

import logging

import cloudinary
import cloudinary.uploader

from app.schemas.config import settings

# Cloudinary SDK config
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


class CloudinaryUploader:  # Wraps Cloudinary SDK — keeps all provider logic in one place.

    def upload(self, file_path: str, folder: str) -> dict:
        response = cloudinary.uploader.upload(file_path, folder=folder)
        return {
            "url": response["secure_url"],
            "width": response.get("width"),
            "height": response.get("height"),
        }

    def delete(self, public_id: str) -> bool:
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
        except Exception:
            logging.exception(f"Failed to delete {public_id}")
            return False
