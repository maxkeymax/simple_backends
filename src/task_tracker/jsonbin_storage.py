from typing import Any, Dict, List, Optional

import requests

from .base_http_client import BaseHTTPClient
from .config import ConfigJSONBin


class JSONBinStorage(BaseHTTPClient):
    def __init__(self) -> None:
        self.bin_id: Optional[str] = None

    def get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Master-Key": ConfigJSONBin.MASTER_KEY,
            "X-Access-Key": ConfigJSONBin.ACCESS_KEY,
        }

    def get_base_url(self) -> str:
        return "https://api.jsonbin.io/v3/b"

    def send_request(self) -> List[Dict[str, Any]]:
        """Загружает задачи из bin"""
        if not self.bin_id:
            return []

        url = f"{self.get_base_url()}/{self.bin_id}/latest"
        headers = self.get_headers()

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Добавлено для обработки ошибок HTTP
        return response.json().get("record", [])

    def save_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Сохраняет задачи, создаёт bin при первом вызове"""
        url = self.get_base_url()
        headers = self.get_headers()

        if not self.bin_id:
            response = requests.post(url, headers=headers, json=tasks)
            response.raise_for_status()
            self.bin_id = response.json()["metadata"]["id"]
        else:
            url = f"{self.get_base_url()}/{self.bin_id}"
            response = requests.put(url, headers=headers, json=tasks)
            response.raise_for_status()

        return response.json().get("record", [])
