import psycopg2
from dotenv import load_dotenv
import os
from typing import Tuple,List

load_dotenv(override=True)

REQUIRED_VARS = ["PHOST", "PDATABASE", "PUSER", "PPASSWORD"]

for var in REQUIRED_VARS:
    if not os.getenv(var):
        raise RuntimeError(f"Missing environment variable: {var}")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("PHOST"),
        database=os.getenv("PDATABASE"),
        user=os.getenv("PUSER"),
        password=os.getenv("PPASSWORD"),
        sslmode="require"
    )
    
def load_db() -> List[Tuple]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM photographs LIMIT 10;")
            return cur.fetchall()    
        
if __name__ == "__main__":
    rows = load_db()
    for row in rows:
        print(row)