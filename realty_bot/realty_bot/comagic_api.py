import json
import random

from datetime import datetime

import requests


async def make_call_request(token: str, name: str, phone_number: str, data: dict, source: str, source_id: str = None, **kwargs):
    """Отправляем заявку в Comagic."""
    url = 'https://dataapi.comagic.ru/v2.0'
    query_id = random.randint(0, 10 ** 6)

    payload = {
        "jsonrpc": "2.0",
        "id": query_id,
        "method": "upload.offline_messages",
        "params": {
            "access_token": token,
            "offline_messages": [
                {
                    "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": f"{name}",
                    "phone": f"{phone_number}",
                    "message": f"{data}",
                    f"{source}": int(source_id)
                }
            ]
        }
    }

    try:
        r = requests.post(url, data=json.dumps(payload))
        # if r.status_code == '200':

    except Exception as e:  # requests.exceptions.MissingSchema
        print(f"Не создал заявку, ошибка {e}")
        return {}
