from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile, MediaGroup

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.about_project import about_project_keyboard
from tgbot.keyboards.building_menu import building, menu_markup
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_about_project_photos


async def maps(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'О проекте'"""
    building_name = callback_data.get('name')
    text = '<b><a href="https://yandex.ru/maps/213/moscow/?from=api-maps&ll=37.635749%2C55.769049&origin=jsapi_2_1_79&pt=37.635539%2C55.769297~37.638521%2C55.769383&z=16">Схема проезда</a></b>'
    await call.message.answer(text=text, reply_markup=await menu_markup(building_name))
    await log_stat(call.from_user, event='Нажатие кнопки "О проекте"')
    await insert_dict(call.from_user, event='Нажатие кнопки "О проекте"')


def register_maps(dp: Dispatcher):
    dp.register_callback_query_handler(maps, building.filter(section='maps'), state='*')
