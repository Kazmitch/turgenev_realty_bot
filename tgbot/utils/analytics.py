import datetime
import logging

from aiogram.types import User
from aioinflux import InfluxDBWriteError, InfluxDBClient


async def log_stat(client: InfluxDBClient, user: User, time: datetime.datetime, event: str = None, error: str = None):
    data = {
        "measurement": "realty_bot_statistics",
        "timestamp": str(time.timestamp()),
        "fields": {
            'username': str(user.username),
            'user_id': str(user.id),
            'first_name': str(user.first_name),
            'last_name': str(user.last_name),
            'language_code': str(user.language_code),
            'full_name': str(user.full_name),
            "intent": str(event),
            "error": str(error)
        },
        'precision': 'ms'
    }
    try:
        await client.write(data)
    except InfluxDBWriteError as ex:
        logging.error(f'InfluxDB write error: {ex}')
