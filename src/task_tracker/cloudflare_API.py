import os

import requests
from dotenv import load_dotenv

load_dotenv()


class CloudflareAPI:
    def __init__(self):
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{os.getenv('Cloudflare_Account_ID')}/ai/run/"
        self.headers = {"Authorization": f"Bearer {os.getenv('Cloudflare_API_Token')}"}
        self.model = "@cf/meta/llama-3-8b-instruct"
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

    def get_llm_answer(self, task):
        user_input_task = {"role": "user", "content": task}
        if len(self.inputs) > 2:
            self.inputs = self.inputs[:2]
        self.inputs.append(user_input_task)
        response = requests.post(
            f"{self.base_url}{self.model}",
            headers=self.headers,
            json={"messages": self.inputs}
        )
        return response.json()["result"]["response"]
    