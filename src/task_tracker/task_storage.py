import json
from typing import Dict, List


class TaskStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_tasks(self) -> List[Dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    def get_all_tasks(self) -> List[Dict]:
        return self.load_tasks()

    def create_task(self, new_task: Dict):
        tasks = self.load_tasks()
        tasks.append(new_task)
        self.save_tasks(tasks)

    def update_task(self, task_id: int, updated_task: Dict):
        tasks = self.load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task.update(updated_task)
                self.save_tasks(tasks)
                return True
        return False

    def delete_task(self, task_id: int):
        tasks = self.load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                tasks.remove(task)
                self.save_tasks(tasks)
                return True
        return False
