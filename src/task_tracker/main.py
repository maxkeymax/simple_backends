from fastapi import FastAPI


app = FastAPI()


tasks = [
    {"id": 1, "title": "Написать код для такст-трекера", "status": "в работе"},
    {"id": 2, "title": "Протестировать API", "status": "не начато"},
]


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(new_task: dict):
    tasks.append(new_task)
    return {"message": "Задача успешно добавлена"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: dict):
    for task in tasks:
        if task["id"] == task_id:
            task.update(updated_task)
            return {"message": f"Задача № {task_id} успешно обновлена"}
    return {"error": f"Задача с № {task_id} не найдена"}


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return {"message": f"Задача № {task_id} успешно удалена"}
    return {"error": f"Задача с № {task_id} не найдена"}
