import asyncio
import logging
from io import BytesIO

from aiogram import Bot, Dispatcher
from aiogram.types import InputFile, InputMediaPhoto, InputMediaVideo
from aiogram.utils import exceptions

from tgbot.config import load_config
from tgbot.utils.dp_api.db_commands import create_mailing, get_mailing
from tgbot.utils.images import get_photo_bytes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"logs/mailing.log")
formatter = logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(message)s", datefmt='%d.%m.%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

config = load_config('.env')
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot)


async def send_message(user_id: int, text: str, photo: str | None, video: str | None, disable_notification: bool = False) -> str | bool:
    """Делаем отправку сообщения."""
    try:
        if photo:
            bytes_photo = BytesIO(await get_photo_bytes(photo))
            file = InputFile(path_or_bytesio=bytes_photo)
            msg = await bot.send_photo(user_id, file, text, disable_notification=disable_notification)
        else:
            msg = await bot.send_video(user_id, video, caption=text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text, photo)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return msg.message_id
    return False


async def broadcaster(users_list: list, text: str, image: str, video: str, mailing_id: str) -> int:
    """Выполняем рассылку."""
    count = 0
    try:
        for user_id in users_list:
            msg_id = await send_message(user_id, text, image, video)
            if msg_id:
                count += 1
                await create_mailing(mailing_id, user_id, msg_id)
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.info(f"{count} messages successful sent.")

    return count


async def edit_message(user_id: str, msg_id: int, text: str, photo: str | None, video: str | None, disable_notification: bool = False) -> bool:
    """Редактируем сообщение."""
    try:
        if photo:
            bytes_photo = BytesIO(await get_photo_bytes(photo))
            file = InputFile(path_or_bytesio=bytes_photo)
            media = InputMediaPhoto(file, caption=text)
        else:
            bytes_video = BytesIO(await get_photo_bytes(video))
            file = InputFile(path_or_bytesio=bytes_video)
            media = InputMediaVideo(file, caption=text)
        await bot.edit_message_media(media=media, chat_id=user_id, message_id=msg_id)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await edit_message(user_id, msg_id, text, photo)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster_edit(mailing_id: str, text: str, image: str, video: str) -> int:
    """Выполняем редактирование рассылки."""
    count = 0
    try:
        for mailing in list(await get_mailing(mailing_id)):
            user_id, msg_id = mailing.user_bot.telegram_id, int(mailing.msg_id)
            if await edit_message(user_id, msg_id, text, image, video):
                count += 1
            await asyncio.sleep(.05)
    finally:
        logger.info(f"{count} messages successful edited.")

    return count


async def delete_message(user_id: str, msg_id: int) -> bool:
    """Удаляем сообщение."""
    try:
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
    except exceptions.BotBlocked:
        logger.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logger.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await delete_message(user_id, msg_id)  # Recursive call
    except exceptions.UserDeactivated:
        logger.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{user_id}]: failed")
    else:
        logger.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster_delete(mailing_id: str) -> int:
    """Выполняем удаление рассылки."""
    count = 0
    try:
        for mailing in list(await get_mailing(mailing_id)):
            user_id, msg_id = mailing.user_bot.telegram_id, int(mailing.msg_id) - 1
            if await delete_message(user_id, msg_id):
                count += 1
        await asyncio.sleep(.05)
    finally:
        logger.info(f"{count} messages successful deleted.")

    return count
