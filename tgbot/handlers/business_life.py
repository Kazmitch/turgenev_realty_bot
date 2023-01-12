from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.business_life import business_life_keyboard
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_business_life_photo, get_about_project_video


async def business_life(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'Апартаменты для бизнеса и жизни'."""
    building_name = callback_data.get('name')
    video = await get_about_project_video(building_name)
    file_video = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{video.video.name}')
    photo = await get_business_life_photo(building_name)
    file_photo = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
    markup = await business_life_keyboard(building_name)
    await call.message.answer_video(video=file_video)
    await call.message.answer_photo(photo=file_photo,
                                    caption=photo.description,
                                    reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "Апартаменты для бизнеса и жизни"')
    await insert_dict(call.from_user, event='Нажатие кнопки "Апартаменты для бизнеса и жизни"')


def register_business_life(dp: Dispatcher):
    dp.register_callback_query_handler(business_life, building.filter(section='business_life'), state='*')
