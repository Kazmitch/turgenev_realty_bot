from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile, MediaGroup

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.about_project import about_project_keyboard
from tgbot.keyboards.building_menu import building
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_about_project_photos


async def presentations(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'О проекте'"""
    building_name = callback_data.get('name')
    photo_set = await get_about_project_photos(building_name)
    album = MediaGroup()
    for photo in photo_set:
        file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
        description = photo.description if photo.description else None
        album.attach_photo(file, caption=description)
    markup = await about_project_keyboard(building_name)
    await call.message.answer_media_group(album)
    await call.message.answer(text='Свяжитесь с нами для более подробной информации', reply_markup=markup)
    await log_stat(call.from_user, event='Нажатие кнопки "О проекте"')
    await insert_dict(call.from_user, event='Нажатие кнопки "О проекте"')


def register_presentations(dp: Dispatcher):
    dp.register_callback_query_handler(presentations, building.filter(section='presentations'), state='*')
