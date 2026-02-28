import psycopg2
from dotenv import load_dotenv
import os
import csv 
from pydantic import ValidationError
from schema.Photo import Photo
import logging

load_dotenv(override=True)

def get_connection():
    REQUIRED_VARS = ["PHOST", "PDATABASE", "PUSER", "PPASSWORD"]
    for var in REQUIRED_VARS:
        if not os.getenv(var):
            raise RuntimeError(f"Missing environment variable: {var}")
    return psycopg2.connect(
        host=os.getenv("PHOST"),
        database=os.getenv("PDATABASE"),
        user=os.getenv("PUSER"),
        password=os.getenv("PPASSWORD"),
        sslmode="require"
    )
 
def view_records():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM photographs LIMIT 10")
                rows = cur.fetchall()
                res = []
                for tuples in rows:
                    res.append(tuples)
        return res
    except Exception as e:
        print(f"DB Fetch failed: {e}") 
                          
def upload_images_from_csv(csv_file):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                with open(csv_file, "r", newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            photo = Photo(
                                id=int(row.get('id', 0)),  
                                filename=row['filename'],
                                url=row['url'],
                                width=int(row.get('width', 1080)),
                                height=int(row.get('height', 1920)),
                                category=row.get('category', "nature")
                            )
                        except ValidationError as ve:
                            print(f"Validation error for row {row}: {ve}")
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
        print(f"Failed to upload CSV to PostgreSQL: {e}")

def upload_photo_to_db(photo: Photo) -> int:
    try:
        with get_connection() as conn:
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
                photo_id = result[0] if result else None
                conn.commit()
                return photo_id
    except Exception as e:
        logging.info(e)
        raise e

def fetch_photographs(limit: int, offset: int):
    try:
        with get_connection() as conn:
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
        logging.info(e)
        raise e
    
if __name__ == "__main__":
    csv_file = "/Users/Patron/Github/portfolio-backend-server/image_metdata.csv"
    upload_images_from_csv(csv_file)
    