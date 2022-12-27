import logging
import random
from datetime import datetime

import requests
from aiogram import Bot

from tgbot.config import load_config

config = load_config('.env')
bot = Bot(token=config.misc.bot_sender_token, parse_mode='HTML')

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/comagic_api.log")
formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s", datefmt='%d.%m.%Y %H:%M:%S')
handler.setFormatter(formatter)
logger2.addHandler(handler)


async def make_comagic_call_request(token: str, name: str, phone_number: str, data: dict, source: str,
                                    source_id: str = None, **kwargs):
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
            text_true = f'Бот: <b>{config.tg_bot.bot_name}</b>\n' \
                        f'✅ Создана заявка\nКод статуса: {r.status_code}\nДанные: {data}'
            await bot.send_message(chat_id=config.misc.chat_info, text=text_true)
            return True
        else:
            logger2.error(f'Статус ответа: {r.status_code}. Не удалось создать заявку с {data}')
            text_false = f'Бот: <b>{config.tg_bot.bot_name}</b>\n' \
                         f'❌ Заявка не создалась\nКод статуса: {r.status_code}\nДанные: {data}'
            await bot.send_message(chat_id=config.misc.chat_info, text=text_false)
            return False
    except Exception as e:  # requests.exceptions.MissingSchema
        logger2.exception(f'Не удалось создать заявку.')
        await bot.send_message(chat_id=config.misc.chat_info, text=f'Бот: <b>{config.tg_bot.bot_name}</b>\n'
                                                                   f'Ошибка при создании заявки\n\n{e}\n\n'
                                                                   f'Данные: {data}')
        return False
