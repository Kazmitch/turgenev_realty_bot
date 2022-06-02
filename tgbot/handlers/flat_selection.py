from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.flat_selection import area_keyboard, price_keyboard, year_keyboard, rooms_keyboard, floor_keyboard, \
    flat_cd, flats_keyboard
from tgbot.states.flat_selection import FlatStates
from tgbot.utils.xml_to_dict import get_offers_yan


async def flats(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку выбора квартиры"""
    building_name = callback_data.get('name')
    await choice_area(call, building_name=building_name)


async def choice_area(call: CallbackQuery, **kwargs):
    """Предлагаем выбрать площадь квартиры."""
    building_name = kwargs.get('building_name')
    markup = await area_keyboard(building_name)
    await call.message.answer(text='Укажите минимальную площадь квартиры/апартаментов', reply_markup=markup)
    await FlatStates.flat_area.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def choice_price(call: Union[CallbackQuery, Message], building_name: str, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем выбрать стоимость квартиры."""
    await state.update_data(building_name=building_name)
    await state.update_data(area=callback_data.get('area'))
    markup = await price_keyboard(building_name)
    await call.message.answer(text='Укажите максимальную цену квартиры/апартаментов', reply_markup=markup)
    await FlatStates.flat_price.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def choice_year(call: Union[CallbackQuery, Message], building_name: str, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем выбрать год сдачи."""
    await state.update_data(price=callback_data.get('price'))
    markup = await year_keyboard(building_name)
    await call.message.answer(text='Срок сдачи квартиры/апартаментов?', reply_markup=markup)
    await FlatStates.flat_year.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def choice_rooms(call: CallbackQuery, building_name: str, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем выбрать количество комнат."""
    await state.update_data(year=callback_data.get('year'))
    markup = await rooms_keyboard(building_name)
    await call.message.answer(text='Количество комнат?', reply_markup=markup)
    await FlatStates.flat_rooms.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def choice_floor(call: CallbackQuery, building_name: str, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем выбрать этаж."""
    await state.update_data(rooms=callback_data.get('rooms'))
    markup = await floor_keyboard(building_name)
    await call.message.answer(text='Какой этаж?', reply_markup=markup)
    await FlatStates.flat_floor.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_flats(call: CallbackQuery, building_name: str, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем квартиры на выбор."""
    await state.update_data(floor=callback_data.get('floor'))
    markup = await flats_keyboard(building_name)
    await call.message.answer(text='Подобрал для вас варианты, смотрим?', reply_markup=markup)
    await FlatStates.flat_data.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def flat_navigate(call: Union[CallbackQuery, Message], callback_data: dict, **kwargs):
    """Функция, обрабатывающая все нажатия на кнопки в меню.

    Args:
        call: Тип объекта Message, который прилетает в хендлер.
        callback_data (dict): словарь с данными, которые хранятся в нажатой кнопке.

    """

    # Название ЖК
    building_name = callback_data.get('building_name')

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get('level')

    # Получаем состояние
    state = kwargs.get('state', '')

    levels = {
        '0': choice_area,  # Отдаем выбор площади
        '1': choice_price,  # Отдаем выбор стоимости
        '2': choice_year,  # Отдаем выбор года
        '3': choice_rooms,  # Отдаем выбор комнат
        '4': choice_floor,  # Отдаем выбор этажа
        '5': show_flats,  # Показываем варианты
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        building_name=building_name,
        state=state,
        callback_data=callback_data,
    )


def register_selection_flat(dp: Dispatcher):
    dp.register_callback_query_handler(flats, building.filter(section='flats'), state='*')
    dp.register_callback_query_handler(flat_navigate, flat_cd.filter(), state='*')
