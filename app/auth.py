"""Admin authentication dependency."""

from fastapi import Header, HTTPException

from app.schemas.config import settings


def verify_admin_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    if not settings.ADMIN_API_KEY or x_api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
