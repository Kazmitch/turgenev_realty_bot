import asyncio
import logging
import os

import django
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
# from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.statistics import InfluxMiddleware


logger = logging.getLogger(__name__)


# def register_all_middlewares(dp):
    # dp.setup_middleware(InfluxMiddleware(influx_client))
    # dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'realty_bot.realty_bot.settings')
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


async def main(all_handlers):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2(config.redis_host) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    # register_all_middlewares(dp)
    register_all_filters(dp)
    all_handlers(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.get_session()


if __name__ == '__main__':
    try:
        setup_django()
        from imported_handlers import register_all_handlers

        asyncio.run(main(register_all_handlers))
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
