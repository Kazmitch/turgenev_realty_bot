from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile, MediaGroup

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.about_project import about_project_keyboard
from tgbot.keyboards.building_menu import building
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_about_project_photos


async def project(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'О проекте'"""
    building_name = callback_data.get('name')
    photo_set = await get_about_project_photos(building_name)
    album = MediaGroup()
    for photo in photo_set:
        file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
        album.attach_photo(file)
    markup = await about_project_keyboard(building_name)
    await call.message.answer_media_group(album)
    text = """HILL8 находится на первой линии проспекта Мира в двух минутах пешком от метро «Алексеевская», в Останкинском районе, с удобным выездом на крупные магистрали.
Архитектура визуального комфорта, которая задает новую планку качества в мировом девелопменте:
- Юрcкий мрамор, окна в пол, французские балконы, открытые террасы, современное инженерное и технологическое наполнение.
- Поэтажное функциональное зонирование многофункционального комплекса HILL8. Распределение потоков посетителей и жильцов
- Элегантное внутреннее убранство лобби и мест общего пользования от дизайнера Карима Рашида
- Высота потолков не менее 3,0 м
- Функциональность планировочных решений"""
    await call.message.answer(text=text, reply_markup=markup)
    await log_stat(call.from_user, event='Нажатие кнопки "О проекте"')
    await insert_dict(call.from_user, event='Нажатие кнопки "О проекте"')


def register_about_project(dp: Dispatcher):
    dp.register_callback_query_handler(project, building.filter(section='project'), state='*')
