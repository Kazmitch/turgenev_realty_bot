import json
import random
import logging

from datetime import datetime

import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"{__name__}.log")
formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s", datefmt='%d.%m.%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


async def make_calltouch_call_request(token: str, site_id: str, name: str, phone_number: str, data: dict):
    """Отправляем заявку в Calltoch."""
    url = 'https://api.calltouch.ru/lead-service/v1/api/request/create'

    query_id = random.randint(0, 10 ** 6)

    headers = {
        'Access-Token': token,
        'SiteId': site_id
    }

    payload = {
        "requests":
            [
                {
                    "requestNumber": query_id,
                    "subject": "Телеграм бот",
                    "requestDate": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "phoneNumber": phone_number,
                    "fio": name,
                    "comment": {
                        "text": f"{data}"
                    }
                }
            ]
    }

    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            logger.info(f'{r.status_code} Создана заявка с {data}')
            return True
        else:
            logger.error(f'{r.status_code} Не удалось создать заявку с {data}')
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        print(f"Не создал заявку, ошибка {e}")
        return False
