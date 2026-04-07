"""Database connection and operations."""

import logging
import os
import csv

import psycopg2
from psycopg2 import pool
from pydantic import ValidationError
from dotenv import load_dotenv

from app.schemas.photo import Photo

load_dotenv(override=True)

# Initialize connection pool
_connection_pool = None


def get_connection_pool():
    """Initialize and return the connection pool."""
    global _connection_pool
    if _connection_pool is None:
        REQUIRED_VARS = ["PHOST", "PDATABASE", "PUSER", "PPASSWORD"]
        for var in REQUIRED_VARS:
            if not os.getenv(var):
                raise RuntimeError(f"Missing environment variable: {var}")

        _connection_pool = pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=10,
            host=os.getenv("PHOST"),
            database=os.getenv("PDATABASE"),
            user=os.getenv("PUSER"),
            password=os.getenv("PPASSWORD"),
            sslmode="require"
        )
    return _connection_pool


def get_connection():
    """Get a connection from the pool."""
    return get_connection_pool().getconn()


def view_records():
    """View recent records from photographs table."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM photographs LIMIT 10")
            rows = cur.fetchall()
            res = []
            for tuples in rows:
                res.append(tuples)
        return res
    except Exception as e:
        logging.exception(e)
        return None
    finally:
        if conn is not None:
            get_connection_pool().putconn(conn)


def upload_images_from_csv(csv_file):
    """Upload images from CSV file to database."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            with open(csv_file, "r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        url_value = row['url']
                        category_value = row.get('category', "nature")
                        photo = Photo(
                            filename=row['filename'],
                            url=url_value,  # type: ignore
                            width=int(row.get('width', 1080)),
                            height=int(row.get('height', 1920)),
                            category=category_value  # type: ignore
                        )
                    except ValidationError as ve:
                        logging.exception(f"Validation error for row {row}")
                        continue

                    cur.execute(
                        """
                        INSERT INTO photographs (filename, url, category, width, height)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id;
                        """,
                        (photo.filename, photo.url, photo.category, photo.width, photo.height)
                    )
                    result = cur.fetchone()
                    photo_id = result[0] if result is not None else None
                    logging.info(f"Inserted {photo.filename} with id {photo_id}")
        conn.commit()
        return {"message": "All photos uploaded successfully"}

    except Exception as e:
        logging.exception(e)
        return None
    finally:
        if conn is not None:
            get_connection_pool().putconn(conn)


def upload_photo_to_db(photo: Photo) -> int:
    """Upload a single photo to the database."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO photographs (filename, url, category, width, height)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (photo.filename, photo.url, photo.category, photo.width, photo.height)
            )
            result = cur.fetchone()
            photo_id: int | None = result[0] if result is not None else None
            conn.commit()
            return photo_id if photo_id is not None else 0
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        if conn is not None:
            get_connection_pool().putconn(conn)


def fetch_photographs(limit: int, offset: int):
    """Fetch photographs from database with pagination."""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, filename, url, category, width, height
                FROM photographs
                ORDER BY id
                LIMIT %s OFFSET %s;
                """,
                (limit, offset)
            )
            rows = cur.fetchall()
            return [
                {
                    "id": r[0],
                    "filename": r[1],
                    "url": r[2],
                    "category": r[3],
                    "width": r[4],
                    "height": r[5]
                }
                for r in rows
            ]
    except Exception as e:
        logging.exception(e)
        return None
    finally:
        if conn is not None:
            get_connection_pool().putconn(conn)


def fetch_local_photos():
    """Read and return photographs from local CSV file."""
    try:
        # Read from the local csv file and return to frontend
        csv_file = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "image_metdata.csv")
        photos = []

        with open(csv_file, newline='', encoding="utf-8") as f:
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

    except Exception as e:
        logging.exception(e)
        return None


if __name__ == "__main__":
    csv_file = "/Users/Patron/Github/portfolio-backend-server/artifacts/image_metdata.csv"
    upload_images_from_csv(csv_file)
