import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

# Database connection parameters
# If running in Docker (same network), hostname is 'database'.
# If running locally (exposed ports), hostname is 'localhost'.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM tasks"))
        tasks = []
        for row in result:
            tasks.append({
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "status": row.status,
                "created_at": row.created_at
            })
    return tasks
