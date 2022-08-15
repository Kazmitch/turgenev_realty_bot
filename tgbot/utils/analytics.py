import logging
from datetime import datetime

from aiogram.types import User
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from tgbot.config import load_config


async def log_stat(user: User, event: str = None, error: str = None):
    config = load_config(".env")

    data = {
        "measurement": "realty_bot_statistics",
        "time": datetime.utcnow(),
        "fields": {"event": 1},
        "tags": {
            'username': str(user.username),
            'user_id': str(user.id),
            'first_name': str(user.first_name),
            'last_name': str(user.last_name),
            'language_code': str(user.language_code),
            'full_name': str(user.full_name),
            "intent": str(event),
            "error": str(error)
        }
    }

    try:
        async with InfluxDBClientAsync(url=config.influxdb.url, token=config.influxdb.token, org=config.influxdb.org) as client:
            write_api = client.write_api()
            ready = await client.ping()
            print(f"InfluxDB: {ready}")
            successfully = await write_api.write(bucket=config.influxdb.bucket, record=data)
            print(f" > successfully: {successfully}")
    except InfluxDBError as ex:
        logging.error(f'InfluxDB write error: {ex}')
