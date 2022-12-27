import json
import logging
import random
from datetime import datetime

import requests
from aiogram import Bot

from tgbot.config import load_config

config = load_config('.env')
bot = Bot(token=config.misc.bot_sender_token, parse_mode='HTML')

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
            text_true = f'Бот: <b>{config.tg_bot.bot_name}</b>\n' \
                        f'✅ Создана заявка\nКод статуса: {r.status_code}\nДанные: {data}'
            await bot.send_message(chat_id=config.misc.chat_info, text=text_true)
            return True
        else:
            logger.error(f'Статус ответа: {r.status_code}. Не удалось создать заявку с {data}')
            text_false = f'Бот: <b>{config.tg_bot.bot_name}</b>\n' \
                         f'❌ Заявка не создалась\nКод статуса: {r.status_code}\nДанные: {data}'
            await bot.send_message(chat_id=config.misc.chat_info, text=text_false)
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        logger.exception(f'Не удалось создать заявку.')
        await bot.send_message(chat_id=config.misc.chat_info, text=f'Бот: <b>{config.tg_bot.bot_name}</b>\n'
                                                                   f'Ошибка при создании заявки:\n{e}\n\n'
                                                                   f'Данные: {data}')
        return False


async def make_calltouch_callback_request(token: str, route_key: str, source: str, name: str, phone_number: str,
                                          data: dict):
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
            logger.info(f'Статус ответа: {r.status_code}. Создан обратный звонок с {data}')
            text_true = f'Бот: <b>{config.tg_bot.bot_name}</b>\n' \
                        f'✅ Создан обратный звонок\nКод статуса: {r.status_code}\nДанные: {data}'
            await bot.send_message(chat_id=config.misc.chat_info, text=text_true)
            return True
        else:
            logger.error(f'Статус ответа: {r.status_code}. Не удалось создать обратный звонок с {data}')
            text_false = f'Бот: <b>{config.tg_bot.bot_name}</b>\n' \
                         f'❌ Обратный звонок не создался\nКод статуса: {r.status_code}\nДанные: {data}'
            await bot.send_message(chat_id=config.misc.chat_info, text=text_false)
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        logger.exception(f'Не удалось создать обратный звонок.')
        await bot.send_message(chat_id=config.misc.chat_info, text=f'Бот: <b>{config.tg_bot.bot_name}</b>\n'
                                                                   f'Ошибка при создании заявки:\n{e}\n\n'
                                                                   f'Данные: {data}')
        return False
