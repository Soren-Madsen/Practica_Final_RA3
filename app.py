from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API de Tareas con FastAPI")

class TaskBase(BaseModel):
    titulo: str
    completada: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True  # para compatibilidad con ORM (opcional)

tasks_db = [
    {"id": 1, "titulo": "Aprender FastAPI", "completada": False},
    {"id": 2, "titulo": "Construir un API CRUD", "completada": False}
]

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_id = max(t["id"] for t in tasks_db) + 1 if tasks_db else 1
    new_task = task.model_dump()  # convierte el modelo Pydantic a dict
    new_task["id"] = new_id
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskCreate):
    for t in tasks_db:
        if t["id"] == task_id:
            t["titulo"] = task_update.titulo
            t["completada"] = task_update.completada
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            tasks_db.pop(i)
            return {"result": "Tarea eliminada"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

