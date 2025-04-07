import requests

from .base_http_client import BaseHTTPClient
from .config import ConfigJSONBin


class JSONBinStorage(BaseHTTPClient):
    def __init__(self):
        self.bin_id = None

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Master-Key": ConfigJSONBin.MASTER_KEY,
            "X-Access-Key": ConfigJSONBin.ACCESS_KEY,
        }

    def get_base_url(self):
        return "https://api.jsonbin.io/v3/b"

    def send_request(self):
        """Загружает задачи из bin"""
        if not self.bin_id:
            return []

        url = f"{self.get_base_url()}/{self.bin_id}/latest"
        headers = self.get_headers()

        response = requests.post(url, headers=headers)
        return response.json().get("record", [])

    def save_tasks(self, tasks):
        """Сохраняет задачи, создаёт bin при первом вызове"""
        url = self.get_base_url()
        headers = self.get_headers()

        if not self.bin_id:
            response = requests.post(url, headers=headers, json=tasks)
            self.bin_id = response.json()["metadata"]["id"]
        else:
            url = f"{self.get_base_url()}/{self.bin_id}"
            response = requests.put(url, headers=headers, json=tasks)
        return response.json().get("record", [])
            