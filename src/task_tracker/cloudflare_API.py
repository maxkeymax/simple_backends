from typing import Dict, List

import requests

from .base_http_client import BaseHTTPClient
from .config import ConfigAPI


class CloudflareAPI(BaseHTTPClient):
    def __init__(self) -> None:
        self.model: str = ConfigAPI.CLOUDFLARE_MODEL
        self.cloudflare_api_token: str = ConfigAPI.CLOUDFLARE_API_TOKEN
        self.cloudflare_acc_id: str = ConfigAPI.CLOUDFLARE_ACCOUND_ID
        self.inputs: List[Dict[str, str]] = ConfigAPI.INPUTS

    def get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.cloudflare_api_token}"}

    def get_base_url(self) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_acc_id}/ai/run/"

    def send_request(self, task: str) -> str:
        inputs: List[Dict[str, str]] = self.inputs.copy()
        inputs.append({"role": "user", "content": task})

        url: str = f"{self.get_base_url()}{self.model}"
        headers: Dict[str, str] = self.get_headers()
        msg_to_llm: Dict[str, List[Dict[str, str]]] = {"messages": inputs}

        response: requests.Response = requests.post(
            url, headers=headers, json=msg_to_llm
        )
        return response.json()["result"]["response"]
