from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.flat_selection import flat_selection_keyboard
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.offers import get_all_offers


async def make_text(building_name: str) -> str:
    """Формируем текст."""
    min_max_values = await get_all_offers(building_name)
    # max_price = f"{int(min_max_values.get('max_price').split('.')[0]):,}"
    # low_price = f"{int(min_max_values.get('low_price').split('.')[0]):,}"
    max_area = min_max_values.get('max_area')
    low_area = min_max_values.get('low_area')
    text = f'Доступные варианты квартир:\n' \
           f'по площади от <b>{low_area} м²</b> до <b>{max_area} м²</b>\n'
    return text


async def flat_selection(call: CallbackQuery, state: FSMContext, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Подобрать апартаменты'."""
    building_name = callback_data.get('name')
    await state.update_data(building_name=building_name)
    text = await make_text(building_name)
    markup = await flat_selection_keyboard(building_name)
    await call.message.answer(text=text, reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "Подобрать апартаменты"')
    await insert_dict(call.from_user, event='Нажатие кнопки "Подобрать апартаменты"')


def register_selection_flat(dp: Dispatcher):
    dp.register_callback_query_handler(flat_selection, building.filter(section='flats'), state='*')
