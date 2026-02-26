import psycopg2
import dotenv
import os

dotenv.load_dotenv()

required_vars = ["PHOST", "PDATABASE", "PUSER", "PPASSWORD"]

for var in required_vars:
    if os.getenv(var) is None:
        raise ValueError(f"Missing environment variable: {var}")

print("All environment variables loaded successfully.")

conn = psycopg2.connect(
    host=os.getenv("PHOST"),
    database=os.getenv("PDATABASE"),
    user=os.getenv("PUSER"),
    password=os.getenv("PPASSWORD"),
    sslmode="require"
)

cur = conn.cursor()

cur.execute("SELECT * FROM photographs;")  
rows = cur.fetchall()                    

for row in rows:
    print(row)

cur.close()
conn.close()