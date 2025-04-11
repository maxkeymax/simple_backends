from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):
    @abstractmethod
    def send_request(self):
        pass

    @abstractmethod
    def get_headers(self):
        pass

    @abstractmethod
    def get_base_url(self):
        pass
