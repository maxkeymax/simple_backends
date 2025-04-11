from typing import Dict, List

from fastapi import FastAPI, HTTPException
from .task_storage import TaskStorage

app = FastAPI()
task_storage = TaskStorage("tasks.json")


@app.get("/tasks", response_model=List[Dict])
def get_tasks():
    return task_storage.get_all_tasks()


@app.post("/tasks")
def create_task(new_task: Dict):
    task_storage.create_task(new_task)
    return {"message": "Задача успешно добавлена"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Dict):
    if task_storage.update_task(task_id, update_task):
        return {"message": f"Задача № {task_id} успешно обновлена"}
    raise HTTPException(status_code=404, detail=f"Задача с № {task_id} не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_storage.delete_task(task_id):
        return {"message": f"Задача № {task_id} успешно удалена"}
    raise HTTPException(status_code=404, detail=f"Задача с № {task_id} не найдена")
