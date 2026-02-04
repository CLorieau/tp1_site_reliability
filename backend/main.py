import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel

app = FastAPI()

# CORS Configuration
origins = [
    "*", # Allow all for simplicity in this dev environment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "database") # Default to docker service name
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM tasks ORDER BY id DESC"))
            tasks = []
            for row in result:
                tasks.append({
                    "id": row.id,
                    "title": row.title,
                    "description": row.description,
                    "status": row.status,
                    "created_at": str(row.created_at)
                })
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []

@app.post("/tasks")
def create_task(task: TaskCreate):
    try:
        with engine.connect() as connection:
            trans = connection.begin()
            try:
                connection.execute(
                    text("INSERT INTO tasks (title, description, status) VALUES (:title, :description, 'pending')"),
                    {"title": task.title, "description": task.description}
                )
                trans.commit()
                return {"status": "created", "task": task.dict()}
            except Exception as e:
                trans.rollback()
                raise e
    except Exception as e:
        print(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    try:
        with engine.connect() as connection:
            trans = connection.begin()
            try:
                update_data = task.dict(exclude_unset=True)
                if not update_data:
                    raise HTTPException(status_code=400, detail="No fields to update")

                set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
                params = update_data.copy()
                params['id'] = task_id

                result = connection.execute(
                    text(f"UPDATE tasks SET {set_clause} WHERE id = :id"),
                    params
                )
                
                if result.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Task not found")
                
                trans.commit()
                return {"status": "updated", "task": update_data}
            except Exception as e:
                trans.rollback()
                raise e
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        with engine.connect() as connection:
            trans = connection.begin()
            try:
                result = connection.execute(
                    text("DELETE FROM tasks WHERE id = :id"),
                    {"id": task_id}
                )
                if result.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Task not found")
                trans.commit()
                return {"status": "deleted", "id": task_id}
            except Exception as e:
                trans.rollback()
                raise e
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))
