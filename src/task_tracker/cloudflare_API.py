import requests

from .base_http_client import BaseHTTPClient
from .config import ConfigAPI


class CloudflareAPI(BaseHTTPClient):
    def __init__(self):
        self.model = ConfigAPI.CLOUDFLARE_MODEL
        self.cloudflare_api_token = ConfigAPI.CLOUDFLARE_API_TOKEN
        self.cloudflare_acc_id = ConfigAPI.CLOUDFLARE_ACCOUND_ID
        self.inputs = ConfigAPI.INPUTS

    def get_headers(self):
        return {"Authorization": f"Bearer {self.cloudflare_api_token}"}

    def get_base_url(self):
        return f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_acc_id}/ai/run/"

    def send_request(self, task):
        inputs = self.inputs.copy()
        inputs.append({"role": "user", "content": task})

        url = f"{self.get_base_url()}{self.model}"
        headers = self.get_headers()
        msg_to_llm = {"messages": inputs}

        response = requests.post(url, headers=headers, json=msg_to_llm)

        return response.json()["result"]["response"]
