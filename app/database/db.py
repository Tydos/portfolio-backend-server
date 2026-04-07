"""Database connection and operations."""

import logging
import os
import csv
from typing import Optional
from psycopg2 import pool
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.photo import Photo


class DatabaseManager:
    """Manages database connections and photograph operations."""

    def __init__(self, db_url: Optional[str] = None):
        """Initialize database manager with PostgreSQL connection URL."""
        self.db_url = db_url or settings.DATABASE_URL
        self.connection_pool = None

    def get_connection_pool(self):
        """Initialize and return the connection pool."""
        if not self.db_url:
            raise RuntimeError("Missing DATABASE_URL environment variable")
        if self.connection_pool is None:
            self.connection_pool = pool.ThreadedConnectionPool(
                minconn=2,
                maxconn=10,
                dsn=self.db_url
            )
        return self.connection_pool

    def close_pool(self):
        """Close the connection pool."""
        if self.connection_pool is not None:
            self.connection_pool.closeall()
            self.connection_pool = None
            logging.info("Database connection pool closed")

    def get_connection(self):
        """Get a connection from the pool."""
        return self.get_connection_pool().getconn()

    def return_connection(self, conn):
        """Return a connection to the pool."""
        if conn is not None:
            self.get_connection_pool().putconn(conn)

    def create_photographs_table(self):
        """Create the photographs table if it doesn't exist."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS photographs (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255) NOT NULL,
                        url VARCHAR(2048) NOT NULL,
                        category VARCHAR(50) DEFAULT 'nature' NOT NULL,
                        width INTEGER NOT NULL DEFAULT 1080,
                        height INTEGER NOT NULL DEFAULT 1920,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            conn.commit()
            logging.info("Photographs table created successfully")
        except Exception:
            if conn:
                conn.rollback()
            logging.exception("Failed to create photographs table")
            raise
        finally:
            self.return_connection(conn)

    def view_records(self):
        """View recent records from photographs table."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM photographs LIMIT 10")
                return cur.fetchall()
        except Exception:
            logging.exception("Failed to view records")
            return None
        finally:
            self.return_connection(conn)

    def upload_images_from_csv(self, csv_file):
        """Upload images from CSV file to database."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                with open(csv_file, "r", newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            url_value = row['url']
                            category_value = row.get('category', "nature").lower()
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
                            (photo.filename.lower(), str(photo.url), photo.category, photo.width, photo.height)
                        )
                        result = cur.fetchone()
                        photo_id = result[0] if result is not None else None
                        logging.info(f"Inserted {photo.filename} with id {photo_id}")
            conn.commit()
            return {"message": "All photos uploaded successfully"}

        except Exception:
            if conn:
                conn.rollback()
            logging.exception("Failed to upload images from CSV")
            return None
        finally:
            self.return_connection(conn)

    def upload_photo_to_db(self, photo: Photo) -> int:
        """Upload a single photo to the database."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO photographs (filename, url, category, width, height)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (photo.filename.lower(), str(photo.url), photo.category, photo.width, photo.height)
                )
                result = cur.fetchone()
                conn.commit()
                return result[0] if result else 0
        except Exception:
            if conn:
                conn.rollback()
            logging.exception("Failed to upload photo to database")
            raise
        finally:
            self.return_connection(conn)

    def fetch_photographs(self, limit: int, offset: int):
        """Fetch photographs from database with pagination."""
        conn = None
        try:
            conn = self.get_connection()
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
                return [
                    {
                        "id": r[0],
                        "filename": r[1],
                        "url": r[2],
                        "category": r[3],
                        "width": r[4],
                        "height": r[5]
                    }
                    for r in cur.fetchall()
                ]
        except Exception:
            logging.exception("Failed to fetch photographs from database")
            return None
        finally:
            self.return_connection(conn)

db = DatabaseManager()
