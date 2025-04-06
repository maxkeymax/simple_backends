import os

from dotenv import load_dotenv

load_dotenv()


class ConfigAPI:
    CLOUDFLARE_API_TOKEN = os.getenv("Cloudflare_API_Token")
    CLOUDFLARE_MODEL = os.getenv("Cloudflare_Model")
    CLOUDFLARE_ACCOUND_ID = os.getenv("Cloudflare_Account_ID")
    INPUTS = [
            {
                "role": "system",
                "content": "Твоя роль - личный ассистент, который советует мне как выполнить поставленную задачу",
            },
            {
                "role": "user",
                "content": "Напиши короткую в 2 или 3 предложения рекомендацию по выполнению ниже приведенной задачи. Ответы пиши на русском языке",
            },
        ]
    
    
class ConfigJSONBin:    
    MASTER_KEY = os.getenv("X_Master_Key")
    ACCESS_KEY = os.getenv("X_Access_Key")
    
