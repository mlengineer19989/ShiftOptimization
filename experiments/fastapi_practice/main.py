from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from databases import Database
from experiment.fastapi_practice.model import Task, Entity


app = FastAPI()
database = Database('sqlite:///tasks.db')

# データベースに接続する
@app.on_event("startup")
async def startup():
    await database.connect()

# データベースとの接続を遮断する
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    query = "INSERT INTO tasks (title, description, completed) VALUES (:title, :description, :completed)"
    values = task.dict()
    task_id = await database.execute(query=query, values=values)
    response = {"id": task_id, **values}
    return JSONResponse(content=response, status_code=201)

@app.get("/tasks/", response_model=List[Task])
async def read_tasks(skip: int = 0, limit: int = 100):
    query = "SELECT * FROM tasks ORDER BY id DESC LIMIT :limit OFFSET :skip"
    tasks = await database.fetch_all(query=query, values={"skip": skip, "limit": limit})
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = :id"
    task = await database.fetch_one(query=query, values={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    query = """
        UPDATE tasks SET title = :title, description = :description, completed = :completed
        WHERE id = :id
    """
    values = {"id": task_id, **task.dict()}
    result = await database.execute(query=query, values=values)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {**values}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id = :id"
    result = await database.execute(query=query, values={"id": task_id})
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
