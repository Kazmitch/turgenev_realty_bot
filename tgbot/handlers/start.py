import base64
import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, InputFile

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.building_menu import main_building_menu
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_building, create_userbot, get_start_campaign, get_announcement


async def start_deep_link(message: Message):
    """Переход сразу в меню конкретного ЖК."""
    args = message.get_args()
    if args:
        values = base64.b64decode(args).decode('UTF-8')
        splited_values = values.split('&')
        if len(splited_values) == 4:
            building_name = values.split('&')[0]
            calltracking = values.split('&')[1].split('=')[1]
            site_id = values.split('&')[2].split('=')[1]
            campaign_id = values.split('&')[3].split('=')[1]
            await create_userbot(message, building_name, calltracking, s_id=site_id, c_id=campaign_id)
            await log_stat(message.from_user, event='Регистрация в боте')
            await insert_dict(message.from_user, event='Регистрация в боте')
        else:
            building_name = values.split('&')[0]
            calltracking = values.split('&')[1].split('=')[1]
            source = values.split('&')[2].split('=')[0]
            source_id = values.split('&')[2].split('=')[1]
            await create_userbot(message, building_name, calltracking, **{source: source_id})
            await log_stat(message.from_user, event='Регистрация в боте')
            await insert_dict(message.from_user, event='Регистрация в боте')
    else:
        campaign = await get_start_campaign()
        building_name = campaign.building.latin_name
        calltracking = campaign.call_tracking_name
        source_id = campaign.get_source_id
        await create_userbot(message, building_name, calltracking, **source_id)
        await log_stat(message.from_user, event='Регистрация в боте')
        await insert_dict(message.from_user, event='Регистрация в боте')
    announcement = await get_announcement(building_name)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{announcement.video.name}')
    markup = await main_building_menu(building_name)
    await message.answer_video(
        video=file,
        caption=announcement.description,
        reply_markup=markup
    )


async def start(message: Message):
    """Предлагаем пользователю ввести название ЖК."""
    await message.answer(text="Перейдите по ссылке или через QR-код.")


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_deep_link, CommandStart(deep_link=re.compile(r"^[a-zA-Z\d_=-]{0,64}$")),
                                state="*")
    dp.register_message_handler(start, CommandStart(), state="*")
