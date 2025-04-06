import os

from dotenv import load_dotenv

from .base_http_client import BaseHTTPClient

load_dotenv()


class JSONBinStorage(BaseHTTPClient):
    def __init__(self):
        super().__init__()
        self.bin_id = None

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Master-Key": os.getenv("X_Master_Key"),
            "X-Access-Key": os.getenv("X_Access_Key"),
        }

    def get_base_url(self):
        return "https://api.jsonbin.io/v3/b"

    def save_tasks(self, tasks):
        """Сохраняет задачи, создаёт bin при первом вызове."""
        if not self.bin_id:
            response = self._send_request("POST", self.get_base_url(), json=tasks)
            self.bin_id = response.json()["metadata"]["id"]
        else:
            self._send_request(
                "PUT", f"{self.get_base_url()}/{self.bin_id}", json=tasks
            )

    def load_tasks(self):
        """Загружает задачи из bin"""
        if not self.bin_id:
            return []

        response = self._send_request(
            "GET", f"{self.get_base_url()}/{self.bin_id}/latest"
        )
        return response.json().get("record", [])
