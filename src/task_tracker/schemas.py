from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    """Базовая схема задачи"""

    title: str
    status: str = "к выполнению"


class TaskCreate(TaskBase):
    """Схема для создания задачи"""

    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""

    title: Optional[str] = None
    status: Optional[str] = None
    ai_advice: Optional[str] = None


class Task(TaskBase):
    """Полная схема задачи для ответа API"""

    id: int
    ai_advice: Optional[str] = None
