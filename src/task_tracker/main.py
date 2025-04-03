from fastapi import FastAPI
from typing import List, Dict
import json


app = FastAPI()


# tasks = [
#     {"id": 1, "title": "Написать код для такст-трекера", "status": "в работе"},
#     {"id": 2, "title": "Протестировать API", "status": "не начато"},
# ]

JSON_FILE = 'tasks.json'


def load_tasks() -> List[Dict]:
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    

def save_tasks(tasks: List[Dict]):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


@app.get("/tasks")
def get_tasks():
    return load_tasks()


@app.post("/tasks")
def create_task(new_task: Dict):
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return {"message": "Задача успешно добавлена"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Dict):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_task)
            save_tasks(tasks)
            return {"message": f"Задача № {task_id} успешно обновлена"}
    return {"error": f"Задача с № {task_id} не найдена"}


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return {"message": f"Задача № {task_id} успешно удалена"}
    return {"error": f"Задача с № {task_id} не найдена"}
