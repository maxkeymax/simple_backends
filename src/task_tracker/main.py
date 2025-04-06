from typing import Dict, List

from fastapi import FastAPI, HTTPException

from .cloudflare_API import CloudflareAPI
from .jsonbin_storage import JSONBinStorage

app = FastAPI()
json_storage = JSONBinStorage()
ai = CloudflareAPI()


@app.get("/tasks", response_model=List[Dict])
def get_tasks():
    return json_storage.load_tasks()


@app.post("/tasks")
def create_task(new_task: Dict):
    ai_resp = ai.get_llm_answer(new_task["Название"])
    new_task["Совет от ИИ"] = ai_resp
    tasks = json_storage.load_tasks()
    tasks.append(new_task)
    json_storage.save_tasks(tasks)
    return {"message": "Задача успешно добавлена"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Dict):
    tasks = json_storage.load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_task)
            json_storage.save_tasks(tasks)
            return {"message": f"Задача № {task_id} успешно обновлена"}
    raise HTTPException(status_code=404, detail=f"Задача с № {task_id} не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = [task for task in json_storage.load_tasks() if task["id"] != task_id]
    json_storage.save_tasks(tasks)
    return {"message": f"Задача № {task_id} успешно удалена"}
