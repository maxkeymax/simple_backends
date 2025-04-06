import os

from dotenv import load_dotenv

from .base_http_client import BaseHTTPClient

load_dotenv()


class CloudflareAPI(BaseHTTPClient):
    def __init__(self):
        super().__init__()
        self.model = "@cf/meta/llama-3-8b-instruct"
        self.cloudflare_api_token = os.getenv("Cloudflare_API_Token")
        self.inputs = [
            {
                "role": "system",
                "content": "Твоя роль - личный ассистент, который советует мне как выполнить поставленную задачу",
            },
            {
                "role": "user",
                "content": "Напиши короткую в 2 или 3 предложения рекомендацию по выполнению ниже приведенной задачи. Ответы пиши на русском языке",
            },
        ]

    def get_headers(self):
        return {"Authorization": f"Bearer {os.getenv('Cloudflare_API_Token')}"}

    def get_base_url(self):
        return f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('Cloudflare_Account_ID')}/ai/run/"

    def get_llm_answer(self, task):
        user_input_task = {"role": "user", "content": task}
        if len(self.inputs) > 2:
            self.inputs = self.inputs[:2]
        self.inputs.append(user_input_task)
        response = self._send_request(
            "POST", f"{self.get_base_url()}{self.model}", json={"messages": self.inputs}
        )
        return response.json()["result"]["response"]
