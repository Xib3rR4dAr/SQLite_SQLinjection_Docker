from fastapi import FastAPI, Request, HTTPException, Header, Query
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI(title="User Info API", version="1.0.0")

# Static API Key
API_KEY = "my-secret-api-key" # API Header value
API_KEY_NAME = "X-API-Key"  # Header name

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cur.execute("INSERT OR IGNORE INTO users VALUES ('1', 'Alice', 'alice@example.com', 'Alice#123!')")
    cur.execute("INSERT OR IGNORE INTO users VALUES ('2', 'Bob', 'bob@example.com', 'Bob^P2$$w0rd')")

    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/v1/users/me/info")
async def get_me_info(
    request: Request,
    user_id: str = Query(..., description="User ID for authentication"),
    x_api_key: str = Header(None)
):
    # Check API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

    # Vulnerable SQL query (SQLi)
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    result = conn.execute(query).fetchone()

    if result:
        return {
            "user_id": result["user_id"],
            "name": result["name"],
            "password": result["password"]
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
