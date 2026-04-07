# CSV-based photo metadata reader.

import csv
import logging
from typing import Optional

from app.core.config import settings


def fetch_local_photos(csv_path: Optional[str] = None) -> list[dict] | None:
    # Read and return photographs from a local CSV file.
    try:
        path = csv_path or settings.METADATA_FILE
        photos: list[dict] = []

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                photos.append({
                    "filename": row["filename"],
                    "url": row["url"],
                    "category": row["category"],
                    "width": int(row["width"]),
                    "height": int(row["height"]),
                })

        return photos

    except Exception:
        logging.exception("Failed to read local photos from CSV")
        return None
