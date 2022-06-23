from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.flat_selection import flat_selection_keyboard, flat_params, flat_selection_cd, \
    type_value_keyboard, show_flat_cd
from tgbot.keyboards.flat_selection import order_flats_keyboard
from tgbot.keyboards.send_contact import contact_markup
from tgbot.states.flat_selection import FlatStates
from tgbot.states.send_contact import ContactStates
from tgbot.utils.offers import get_max_and_low_values, get_all_offers


async def make_text(building_name: str, chosen_params: dict) -> str:
    """Формируем текст."""

    min_max_values = await get_all_offers(building_name)
    max_price = min_max_values.get('max_price')[:-6]
    low_price = min_max_values.get('low_price')[:-6]
    max_area = min_max_values.get('max_area')
    low_area = min_max_values.get('low_area')
    area = int(chosen_params.get('flat_area'))
    price = int(chosen_params.get('flat_price'))
    year = int(chosen_params.get('flat_year'))
    rooms = int(chosen_params.get('flat_rooms'))
    text = f'Доступные варианты:\n' \
           f'квартиры от {low_price} до {max_price} млн.р.\n' \
           f'и по площади от {low_area} до {max_area} кв.м\n' \
           f'\n' \
           f'Выбранные параметры:\n' \
           f'Общая площадь от: {area if area != 0 else "все варианты"}\n' \
           f'Цена до: {price if price != 0 else "все варианты"}\n' \
           f'Год сдачи объекта: {year if year != 0 else "все варианты"}\n' \
           f'Количество комнат: {rooms if rooms != 0 else "все варианты"}\n' \
           f'\n' \
           f'Чтобы начать подбор, нажмите кнопку "Показать предложения"'
    return text


async def flat_selection(call: Union[CallbackQuery, Message], state: FSMContext = None, values: dict = None,
                         callback_data: dict = None, **kwargs):
    """Хендлер на кнопку 'Подобрать квартиры'."""
    params = {
        'flat_area': 0,
        'flat_price': 0,
        'flat_year': 0,
        'flat_rooms': 0
    }
    if callback_data:
        try:
            data = await state.get_data()
            params.update(data.get('params'))
            await state.update_data(building_name=callback_data.get('name'))
            building_name = callback_data.get('name')
        except TypeError:
            await state.update_data(building_name=callback_data.get('name'))
            building_name = callback_data.get('name')
    else:
        data = await state.get_data()
        building_name = data.get('building_name')

    if values:
        data = await state.get_data()
        params.update(data.get('params'))
        params.update(values)
    data = await state.get_data()
    await state.update_data(params=params)
    text = await make_text(building_name, params)
    markup = await flat_selection_keyboard(building_name)
    if isinstance(call, CallbackQuery):
        await call.message.answer(text=text, reply_markup=markup)
        await call.message.delete()
    else:
        msg_id = int(data.get('msg_id'))
        message = call
        await message.answer(text=text, reply_markup=markup)
        await message.bot.delete_message(message.chat.id, msg_id)
        await message.delete()


async def type_params(call: Union[CallbackQuery, Message], state: FSMContext, error: bool = False,
                      callback_data: dict = None,
                      **kwargs):
    """Ввести значения."""

    if error:
        data = await state.get_data()
        option = data.get('option')
        building_name = data.get('building_name')
        texts = {
            'flat_area': 'Кажется вы ошиблись(\n'
                         '\n'
                         'Введите желаемую площадь, например: <b>25</b>',
            'flat_price': 'Кажется вы ошиблись(\n'
                          '\n'
                          'Введите желаемую стоимость, например: <b>30</b>',
            'flat_year': 'Кажется вы ошиблись(\n'
                         '\n'
                         'Введите год сдачи, например: <b>2022</b>',
            'flat_rooms': 'Кажется вы ошиблись(\n'
                          '\n'
                          'Введите количество комнат, например: <b>2</b>',
        }
        text = texts.get(option)
        msg_id = int(data.get('msg_id'))
        markup = await type_value_keyboard(building_name)
        message = call
        msg = await message.answer(text=text, reply_markup=markup)
        await message.bot.delete_message(message.chat.id, msg_id)
        await message.delete()
        await state.update_data(msg_id=msg.message_id)
    else:

        option = callback_data.get('option')
        await state.update_data(option=option)
        building_name = callback_data.get('building_name')

        texts = {
            'flat_area': 'Введите желаемую площадь, например: <b>25</b>',
            'flat_price': 'Введите желаемую стоимость, например: <b>30</b>',
            'flat_year': 'Введите год сдачи, например: <b>2022</b>',
            'flat_rooms': 'Введите количество комнат, например: <b>2</b>',
        }
        text = texts.get(option)
        markup = await type_value_keyboard(building_name)
        msg = await call.message.answer(text=text, reply_markup=markup)
        await state.update_data(msg_id=msg.message_id)
        await call.message.delete()
    if option == 'flat_area':
        await FlatStates.flat_area.set()
    if option == 'flat_price':
        await FlatStates.flat_price.set()
    if option == 'flat_year':
        await FlatStates.flat_year.set()
    if option == 'flat_rooms':
        await FlatStates.flat_rooms.set()


async def update_params(message: Union[CallbackQuery, Message], state: FSMContext, callback_data: dict = None,
                        **kwargs):
    """Обновляем введенные данные."""

    state_name = await state.get_state()
    key = state_name.split(':')[1]
    if isinstance(message, Message):
        try:
            value = message.text
            int(value)
            if key == 'flat_year' and len(value) != 4:
                await type_params(message, state=state, error=True)
            else:
                chosen_params = {key: value}
                await flat_selection(message, state=state, values=chosen_params)
        except ValueError:
            await type_params(message, state=state, error=True)
    else:
        value = callback_data.get('param')
        chosen_params = {key: value}
        await flat_selection(message, state=state, values=chosen_params)


async def show_flats(call: CallbackQuery, state: FSMContext, callback_data: dict, **kwargs):
    """Предлагаем квартиры на выбор."""
    data = await state.get_data()
    building_name = data.get('building_name')
    params = data.get('params')
    try:
        min_max_values = await get_max_and_low_values(building_name=building_name, params=params)
        max_price = min_max_values.get('max_price')[:-6]
        low_price = min_max_values.get('low_price')[:-6]
        max_area = min_max_values.get('max_area')
        low_area = min_max_values.get('low_area')
        markup = await order_flats_keyboard(building_name)
        await call.message.answer(text=f'Подобрал для вас варианты квартир:\n'
                                       f'по стоимости от <b>{low_price} млн руб.</b> до <b>{max_price} млн руб.</b>\n'
                                       f'и площади от <b>{low_area} м²</b> до <b>{max_area} м²</b>',
                                  reply_markup=markup)
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


def register_selection_flat(dp: Dispatcher):
    dp.register_callback_query_handler(flat_selection, building.filter(section='flats'),
                                       state=[FlatStates.flat_data, FlatStates.flat_area, FlatStates.flat_price,
                                              FlatStates.flat_year, FlatStates.flat_rooms])
    dp.register_callback_query_handler(type_params, flat_selection_cd.filter(), state='*')
    dp.register_callback_query_handler(update_params, flat_params.filter(),
                                       state=[FlatStates.flat_area, FlatStates.flat_price, FlatStates.flat_year,
                                              FlatStates.flat_rooms])
    dp.register_message_handler(update_params, state=[FlatStates.flat_area, FlatStates.flat_price, FlatStates.flat_year,
                                                      FlatStates.flat_rooms])
    dp.register_callback_query_handler(show_flats, show_flat_cd.filter(), state='*')
