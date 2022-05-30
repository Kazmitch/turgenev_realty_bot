from typing import Union

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.flat_selection import area_keyboard, price_keyboard
from tgbot.states.flat_selection import FlatStates


async def flats(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку выбора квартиры"""
    building_name = callback_data.get('name')
    await choice_area(call)


async def choice_area(call: CallbackQuery, **kwargs):
    """Предлагаем выбрать площадь квартиры."""
    markup = await area_keyboard()

    await call.message.answer(text='Укажите минимальную площадь квартиры/апартаментов', reply_markup=markup)
    # await FlatStates.flat_area.set()


async def choice_price(message: Union[CallbackQuery, Message]):
    """Предлагаем выбрать стоимость квартиры."""
    if isinstance(message, Message):
        area = message.text
        markup = await price_keyboard(area)
        await message.answer(text='Укажите максимальную цену квартиры/апартаментов', reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        area = call.data
        markup = await price_keyboard(area)
        await call.message.answer(text='Укажите максимальную цену квартиры/апартаментов', reply_markup=markup)


def register_selection_flat(dp: Dispatcher):
    dp.register_callback_query_handler(flats, building.filter(section='flats'), state='*')
