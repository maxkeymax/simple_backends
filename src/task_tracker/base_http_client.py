from abc import ABC, abstractmethod

import requests


class BaseHTTPClient(ABC):
    def __init__(self):
        self.base_url = self.get_base_url()
        self.headers = self.get_headers()

    def _send_request(self, method, url, data=None, json=None):
        response = requests.request(
            method, url, headers=self.headers, data=data, json=json
        )
        response.raise_for_status()
        return response

    @abstractmethod
    def get_headers(self):
        pass

    @abstractmethod
    def get_base_url(self):
        pass
