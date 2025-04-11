from typing import Dict, List

from fastapi import HTTPException

from .cloudflare_API import CloudflareAPI
from .jsonbin_storage import JSONBinStorage
from .logging_config import setup_logger
from .schemas import Task, TaskCreate, TaskUpdate

error_logger = setup_logger()


class TaskService:
    """Сервис для работы с задачами."""

    def __init__(self, storage: JSONBinStorage, ai_client: CloudflareAPI):
        self.storage = storage
        self.ai_client = ai_client

    def get_all_tasks(self) -> List[Task]:
        """Получение всех задач."""
        try:
            return self.storage.send_request()
        except Exception as e:
            error_logger.error(f"Ошибка при загрузке задач: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при загрузке задач")

    def create_task(self, task: TaskCreate) -> Dict:
        """Создание новой задачи с рекомендацией от ИИ."""
        try:
            tasks = self.storage.send_request()

            # Генерация ID
            new_id = 1
            if tasks:
                new_id = max(task.get("id", 0) for task in tasks) + 1

            # Формирование новой задачи
            task_dict = task.model_dump()
            task_dict["id"] = new_id

            # Получение рекомендации от ИИ
            try:
                ai_resp = self.ai_client.send_request(task.title)
                task_dict["ai_advice"] = ai_resp
            except Exception as e:
                error_logger.error(f"Ошибка при получении рекомендации от ИИ: {str(e)}")
                task_dict["ai_advice"] = "Не удалось получить рекомендацию"

            tasks.append(task_dict)
            self.storage.save_tasks(tasks)

            return {"message": f"Задача № {new_id} успешно добавлена"}
        except Exception as e:
            error_logger.error(f"Ошибка при создании задачи: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при создании задачи")

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        """Обновление задачи."""
        try:
            tasks = self.storage.send_request()

            for t in tasks:
                if t["id"] == task_id:
                    update_data = task_update.model_dump(exclude_unset=True)

                    if "title" in update_data:
                        new_title = update_data["title"]
                        if t["title"] != new_title:
                            try:
                                update_data["ai_advice"] = self.ai_client.send_request(
                                    new_title
                                )
                            except Exception as e:
                                error_logger.error(
                                    f"Ошибка при получении рекомендации от ИИ: {str(e)}"
                                )
                                update_data["ai_advice"] = (
                                    "Не удалось обновить рекомендацию"
                                )

                    t.update(update_data)
                    self.storage.save_tasks(tasks)
                    return t

            raise HTTPException(
                status_code=404, detail=f"Задача с № {task_id} не найдена"
            )
        except Exception as e:
            error_logger.error(f"Ошибка при обновлении задачи: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при обновлении задачи")

    def delete_task(self, task_id: int) -> Dict:
        try:
            tasks = self.storage.send_request()
            old_len = len(tasks)
            
            updated_tasks = [task for task in tasks if task["id"] != task_id]

            if old_len == len(updated_tasks):
                raise HTTPException(
                    status_code=404, detail=f"Задача с № {task_id} не найдена"
                )

            self.storage.save_tasks(updated_tasks)
            return {"message": f"Задача № {task_id} успешно удалена"}

        except Exception as e:
            error_logger.error(f"Ошибка при удалении задачи: {str(e)}")
            raise HTTPException(status_code=500, detail="Ошибка при удалении задачи")
