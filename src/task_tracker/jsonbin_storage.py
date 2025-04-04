import os

import requests
from dotenv import load_dotenv

load_dotenv()


class JSONBinStorage:
    def __init__(self):
        self.master_key = os.getenv("X_Master_Key")
        self.access_key = os.getenv("X_Access_Key")
        self.bin_id = None
        self.base_url = "https://api.jsonbin.io/v3/b"

    def save_tasks(self, tasks):
        """Сохраняет задачи, создаёт bin при первом вызове."""
        if not self.bin_id:
            response = requests.post(
                self.base_url,
                json=tasks,
                headers={
                    "Content-Type": "application/json",
                    "X-Master-Key": self.master_key,
                    "X-Access-Key": self.access_key,
                },
            )
            self.bin_id = response.json()["metadata"]["id"]
        else:
            requests.put(
                f"{self.base_url}/{self.bin_id}",
                json=tasks,
                headers={
                    "Content-Type": "application/json",
                    "X-Master-Key": self.master_key,
                    "X-Access-Key": self.access_key,
                },
            )
        
    def load_tasks(self):
        '''Загружает задачи из bin'''
        if not self.bin_id:
            return []
        
        response = requests.get(
                f'{self.base_url}/{self.bin_id}/latest',
                headers={
                    "X-Master-Key": self.master_key,
                    "X-Access-Key": self.access_key,
                },
            )
        return response.json().get("record", [])
