from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.about_project import about_project_keyboard
from tgbot.keyboards.building_menu import building
from tgbot.utils.analytics import log_stat
from tgbot.utils.dp_api.db_commands import get_developer_description, get_about_project_photo


async def project(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'О проекте'"""
    building_name = callback_data.get('name')
    description = await get_developer_description(building_name)
    path = await get_about_project_photo(building_name)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{path}')
    markup = await about_project_keyboard(building_name)
    await call.message.answer_photo(photo=file,
                                    caption=description,
                                    reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "О проекте"')


def register_about_project(dp: Dispatcher):
    dp.register_callback_query_handler(project, building.filter(section='project'), state='*')
