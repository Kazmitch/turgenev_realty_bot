from typing import Union

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.flat_selection import area_keyboard, price_keyboard, year_keyboard, rooms_keyboard, floor_keyboard, \
    flat_cd
from tgbot.states.flat_selection import FlatStates


async def flats(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку выбора квартиры"""
    building_name = callback_data.get('name')
    await choice_area(call, building_name=building_name)


async def choice_area(call: CallbackQuery, **kwargs):
    """Предлагаем выбрать площадь квартиры."""
    building_name = kwargs.get('building_name')
    markup = await area_keyboard(building_name)

    # if isinstance(message, Message):
    #     await message.answer(text='Укажите минимальную площадь квартиры/апартаментов', reply_markup=markup)
    #
    # elif isinstance(message, CallbackQuery):
    #     call = message
    #     await call.message.answer(text='Укажите минимальную площадь квартиры/апартаментов', reply_markup=markup)
    # await FlatStates.flat_area.set()
    await call.message.answer(text='Укажите минимальную площадь квартиры/апартаментов', reply_markup=markup)


async def choice_price(message: Union[CallbackQuery, Message], building_name: str, area: str, **kwargs):
    """Предлагаем выбрать стоимость квартиры."""
    if isinstance(message, Message):
        area = message.text
        markup = await price_keyboard(area, building_name)
        await message.answer(text='Укажите максимальную цену квартиры/апартаментов', reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        # area = call.data
        markup = await price_keyboard(area, building_name)
        await call.message.answer(text='Укажите максимальную цену квартиры/апартаментов', reply_markup=markup)


async def choice_year(message: Union[CallbackQuery, Message], building_name: str, area: str, price: str, **kwargs):
    """Предлагаем выбрать год сдачи."""
    if isinstance(message, Message):
        # price = message.text
        markup = await year_keyboard(area, price, building_name)
        await message.answer(text='Срок сдачи квартиры/апартаментов?', reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        markup = await year_keyboard(area, price, building_name)
        await call.message.answer(text='Срок сдачи квартиры/апартаментов?', reply_markup=markup)


async def choice_rooms(call: CallbackQuery, building_name: str, area: str, price: str, year: str, **kwargs):
    """Предлагаем выбрать количество комнат."""
    markup = await rooms_keyboard(area, price, year, building_name)

    await call.message.answer(text='Количество комнат?', reply_markup=markup)


async def choice_floor(call: CallbackQuery, building_name: str, area: str, price: str, year: str, rooms: str, **kwargs):
    """Предлагаем выбрать этаж."""
    markup = await floor_keyboard(area, price, year, rooms, building_name)
    await call.message.answer(text='Какой этаж?', reply_markup=markup)


async def show_flats(call: CallbackQuery, building_name: str, area: str, price: str, year: str, rooms: str, floor: str):
    """Предлагаем квартиры на выбор."""
    await call.message.answer(f'Вы выбрали {building_name}: {area}, {price}, {year}, {rooms}, {floor}')


async def flat_navigate(message: Union[CallbackQuery, Message], callback_data: dict, **kwargs):
    """Функция, обрабатывающая все нажатия на кнопки в меню.

    Args:
        message: Тип объекта Message, который прилетает в хендлер.
        callback_data (dict): словарь с данными, которые хранятся в нажатой кнопке.

    """

    await message.answer(text='Hi')

    # Название ЖК
    building_name = callback_data.get('building_name')

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get('level')

    # Получаем площадь, которую выбрал пользователь
    area = callback_data.get('area')

    # Получаем стоимость, которую выбрал пользователь
    price = callback_data.get('price')

    # Получаем год, который выбрал пользователь
    year = callback_data.get('year')

    # Получаем количество комнат, которое выбрал пользователь
    rooms = callback_data.get('rooms')

    # Получаем этаж, который выбрал пользователь
    floor = callback_data.get('floor')

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
        message,
        building_name=building_name,
        area=area,
        price=price,
        year=year,
        rooms=rooms,
        floor=floor
    )


def register_selection_flat(dp: Dispatcher):

    dp.register_callback_query_handler(flats, building.filter(section='flats'), state='*')
    dp.register_message_handler(flat_navigate, flat_cd.filter(), state='*')
    dp.register_callback_query_handler(flat_navigate, flat_cd.filter(), state='*')

    # dp.register_callback_query_handler(choice_area, state='*')
