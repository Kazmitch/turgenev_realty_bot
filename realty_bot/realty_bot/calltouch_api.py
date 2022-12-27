import json
import random
import logging

from datetime import datetime

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/calltouch_api.log")
formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s", datefmt='%d.%m.%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


async def make_calltouch_call_request(token: str, site_id: str, source: str, name: str, phone_number: str, data: dict):
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
                    "subject": source,
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
            logger.info(f'Статус ответа: {r.status_code}. Создана заявка с {data}')
            return True
        else:
            logger.error(f'Статус ответа: {r.status_code}. Не удалось создать заявку с {data}')
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        logger.exception(f'Не удалось создать заявку.')
        return False


async def make_calltouch_callback_request(token: str, route_key: str, source: str, name: str, phone_number: str, data: dict):
    """Отправляем звонок на перезвон в Calltoch."""
    url = 'https://api.calltouch.ru/widget-service/v1/api/widget-request/user-form/create'

    headers = {
        'Host': 'api.calltouch.ru',
        'Access-Token': token
    }

    payload = {
        "routeKey": route_key,
        "phone": phone_number,
        "fields": [
            {"name": "Имя",
             "value": name},
            {"name": "Дополнительная информация",
             "value": f"{data}"}
        ],
        "scheduleTime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "utmSource": source,
        "utmMedium": source,
        "utmCampaign": source
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        print(f"Не создал заявку, ошибка {e}")
        return False
