import logging
from io import BytesIO

import cloudinary
import cloudinary.uploader
import httpx
from PIL import Image
from supabase import create_client, Client

from app.schemas.config import settings

logger = logging.getLogger(__name__)


class CloudinaryUploader:

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
            logger.exception("Failed to delete %s", public_id)
            return False


class SupabaseUploader:

    def __init__(self):
        self._client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self._bucket = settings.SUPABASE_BUCKET

    def upload(self, file_bytes: bytes, filename: str) -> dict:
        key = filename
        with Image.open(BytesIO(file_bytes)) as img:
            width, height = img.size
        upload_url = f"{settings.SUPABASE_URL}/storage/v1/object/{self._bucket}/{key}"
        response = httpx.post(
            upload_url,
            content=file_bytes,
            headers={
                "Authorization": f"Bearer {settings.SUPABASE_KEY}",
                "Content-Type": "image/jpeg",
            },
        )
        if not response.is_success:
            raise RuntimeError(f"Supabase {response.status_code}: {response.text}")
        public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{self._bucket}/{key}"
        return {"url": public_url, "width": width, "height": height, "storage_key": key}

    def delete(self, storage_key: str) -> bool:
        try:
            self._client.storage.from_(self._bucket).remove([storage_key])
            return True
        except Exception:
            logger.exception("Failed to delete %s", storage_key)
            return False
