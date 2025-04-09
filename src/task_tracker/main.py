import logging
from functools import lru_cache
from typing import List

from fastapi import Depends, FastAPI, HTTPException

from .cloudflare_API import CloudflareAPI
from .jsonbin_storage import JSONBinStorage
from .logging_config import setup_logger
from .schemas import Task, TaskCreate, TaskUpdate
from .task_service import TaskService

app = FastAPI()
error_logger = setup_logger()


@lru_cache()
def get_storage():
    """Фабрика для создания экземпляра хранилища."""
    try:
        return JSONBinStorage()
    except Exception as e:
        error_logger.error(f"Ошибка инициализации JSONBinStorage: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к хранилищу")


@lru_cache()
def get_ai_client():
    """Фабрика для создания экземпляра AI-клиента."""
    try:
        return CloudflareAPI()
    except Exception as e:
        error_logger.error(f"Ошибка инициализации CloudflareAPI: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к AI-сервису")


def get_task_service(
    storage: JSONBinStorage = Depends(get_storage),
    ai_client: CloudflareAPI = Depends(get_ai_client),
):
    return TaskService(storage, ai_client)


@app.get("/tasks", response_model=List[Task], tags="Список всех задач")
def get_tasks(task_service=Depends(get_task_service)):
    return task_service.get_all_tasks()


@app.post("/tasks", tags="Добавление новой задачи")
def create_task(new_task: TaskCreate, task_service=Depends(get_task_service)):
    return task_service.create_tusk(new_task)


@app.put("/tasks/{task_id}", response_model=Task, tags="Обновление задачи")
def update_task(
    task_id: int,
    task: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.update_task(task_id, task)


@app.delete("/tasks/{task_id}", tags="Удаление задачи")
def delete_task(task_id: int, task_service=Depends(get_task_service)):
    return task_service.delete_task(task_id)
