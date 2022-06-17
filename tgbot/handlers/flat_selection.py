from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.flat_selection import area_keyboard, price_keyboard, year_keyboard, rooms_keyboard, \
    flat_cd, flats_keyboard, order_flats_keyboard
from tgbot.keyboards.send_contact import contact_markup
from tgbot.states.flat_selection import FlatStates
from tgbot.states.send_contact import ContactStates
from tgbot.utils.offers import get_offers_yan, get_max_and_low_values


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


async def show_flats(call: CallbackQuery, building_name: str, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем квартиры на выбор."""
    await state.update_data(rooms=callback_data.get('rooms'))
    data = await state.get_data()
    try:
        min_max_values = await get_max_and_low_values(data)
        max_price = min_max_values.get('max_price')[:-6]
        low_price = min_max_values.get('low_price')[:-6]
        max_area = min_max_values.get('max_area')
        low_area = min_max_values.get('low_area')
        markup = await order_flats_keyboard(building_name)
        await call.message.answer(text=f'Подобрал для вас варианты квартир:\n'
                                       f'по стоимости от <b>{low_price} млн руб.</b> до <b>{max_price} млн руб.</b>\n'
                                       f'и площади от <b>{low_area} м²</b> до <b>{max_area} м²</b>', reply_markup=markup)
        await FlatStates.flat_data.set()
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.delete()
    except ValueError:
        markup = await contact_markup(building_name)
        await call.message.answer(text='К сожалению, не смогли найти квартиры по данным параметрам.\n'
                                       'Давайте поможем вам подобрать', reply_markup=markup)
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.delete()
        await ContactStates.building_name.set()


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
        '4': show_flats,  # Показываем варианты
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
