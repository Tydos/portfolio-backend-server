"""Configuration module for the application."""

import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings:
    """Application settings."""

    # API Configuration
    API_TITLE = "Portfolio Backend Server"
    API_DESCRIPTION = "Vercel + FastAPI API Gateway for Portfolio"
    API_VERSION = "1.0.0"

    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "images")

    # CORS Configuration
    CORS_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    # Admin Authentication
    ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")

settings = Settings()
