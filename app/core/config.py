"""Configuration module for the application."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    # API Configuration
    API_TITLE = "Portfolio Backend Server"
    API_DESCRIPTION = "Vercel + FastAPI API Gateway for Portfolio"
    API_VERSION = "1.0.0"

    # Database Configuration
    DB_HOST = os.getenv("PHOST")
    DB_NAME = os.getenv("PDATABASE")
    DB_USER = os.getenv("PUSER")
    DB_PASSWORD = os.getenv("PPASSWORD")

    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # CORS Configuration
    CORS_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    # File Paths
    IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "images")
    METADATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "image_metdata.csv")


settings = Settings()
