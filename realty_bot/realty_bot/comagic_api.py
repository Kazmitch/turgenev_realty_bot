import json
import logging
import random

from datetime import datetime

import requests


logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/comagic_api.log")
formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s", datefmt='%d.%m.%Y %H:%M:%S')
handler.setFormatter(formatter)
logger2.addHandler(handler)


async def make_comagic_call_request(token: str, name: str, phone_number: str, data: dict, source: str, source_id: str = None, **kwargs):
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
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            logger2.info(f'Статус ответа: {r.status_code}. Создана заявка с {data}')
            return True
        else:
            logger2.error(f'Статус ответа: {r.status_code}. Не удалось создать заявку с {data}')
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        logger2.exception(f'Не удалось создать заявку.')
        return False
