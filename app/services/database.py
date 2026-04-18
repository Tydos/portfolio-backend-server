"""Database connection and operations."""

import logging
from contextlib import contextmanager
from typing import Optional

from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from app.schemas.config import settings
from app.schemas.photo import Photo

logger = logging.getLogger("app").getChild(__name__)


class DatabaseManager:
    """Manages database connections and photograph operations."""

    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or settings.DATABASE_URL
        self.connection_pool = None

    def get_connection_pool(self):
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
        if self.connection_pool is not None:
            self.connection_pool.closeall()
            self.connection_pool = None
            logger.info("Database connection pool closed")

    def get_connection(self):
        return self.get_connection_pool().getconn()

    def return_connection(self, conn):
        if conn is not None:
            self.get_connection_pool().putconn(conn)

    @contextmanager
    def _connection(self):
        conn = self.get_connection()
        try:
            yield conn
        finally:
            self.return_connection(conn)

    def create_photographs_table(self):
        with self._connection() as conn:
            try:
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
                logger.info("Photographs table created successfully")
            except Exception:
                conn.rollback()
                logger.exception("Failed to create photographs table")
                raise

    def ping(self) -> bool:
        try:
            with self._connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            return True
        except Exception:
            logger.exception("Database ping failed")
            return False

    def _photo_to_tuple(self, photo: Photo) -> tuple:
        return (photo.filename.lower(), str(photo.url), photo.category, photo.width, photo.height)

    def filename_exists(self, filename: str) -> bool:
        with self._connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM photographs WHERE filename = %s LIMIT 1", (filename,))
                return cur.fetchone() is not None

    def upload_photo_to_db(self, photo: Photo) -> int:
        with self._connection() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO photographs (filename, url, category, width, height)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id;
                        """,
                        self._photo_to_tuple(photo)
                    )
                    result = cur.fetchone()
                conn.commit()
                return result[0] if result else 0
            except Exception:
                conn.rollback()
                logger.exception("Failed to upload photo to database")
                raise

    def fetch_photographs(self, limit: int, offset: int):
        with self._connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, filename, url, category, width, height
                    FROM photographs
                    ORDER BY id
                    LIMIT %s OFFSET %s;
                    """,
                    (limit, offset)
                )
                return [dict(r) for r in cur.fetchall()]


db = DatabaseManager()
