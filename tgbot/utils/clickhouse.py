from aiogram.types import User
from asynch import connect
from asynch.cursors import DictCursor
from datetime import datetime

from tgbot.config import load_config


async def connect_database():
    config = load_config('.env')
    try:
        conn = await connect(
            host=config.misc.clickhouse_post,
            port=config.misc.clickhouse_port,
            database=config.misc.clickhouse_db,
            user=config.misc.clickhouse_user,
            password=config.misc.clickhouse_password,
        )
        return conn
    except Exception as e:
        print(f'connect {e}')


async def create_table(conn):
    try:
        async with conn.cursor(cursor=DictCursor) as cursor:
            await cursor.execute('create database if not exists big_data')
            await cursor.execute("""
            CREATE TABLE if not exists big_data.realty_bot
                (
                    `bot_name`       String,
                    `telegram_id`  String,
                    `telegram_username`     String,
                    `telegram_first_name` String,
                    `telegram_last_name`    String,
                    `phone_number`     String,
                    `intent`   String,
                    `error`   String,
                    `created_at`   String
                )
                ENGINE = MergeTree
                ORDER BY created_at
                    """
                                 )
    except Exception as e:
        print(f'create {e}')


async def insert_dict(user: User, event: str = None, error: str = None, phone_number: str = None):
    try:
        config = load_config('.env')
        conn = await connect_database()
        await create_table(conn)
        async with conn.cursor(cursor=DictCursor) as cursor:
            ret = await cursor.execute(
                """INSERT INTO big_data.realty_bot(bot_name,telegram_id,telegram_username,telegram_first_name,telegram_last_name,phone_number,intent,error,created_at) VALUES""",
                [
                    {
                        "bot_name": str(config.tg_bot.bot_name),
                        "telegram_id": str(user.id),
                        "telegram_username": str(user.username),
                        "telegram_first_name": str(user.first_name),
                        "telegram_last_name": str(user.last_name),
                        "phone_number": str(phone_number),
                        "intent": str(event),
                        "error": str(error),
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ],
            )
            assert ret == 1
    except Exception as e:
        print(f'insert {e}')
