from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.send_contact import contact_button

order_cd = CallbackData('order', 'building_name', 'sort')
flat_selection_cd = CallbackData('selection', 'building_name', 'option')
show_flat_cd = CallbackData('show', 'building_name', 'option')
flat_params = CallbackData('params', 'building_name', 'param')


async def flat_selection_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Подобрать квартиру'."""

    markup = InlineKeyboardMarkup(row_width=2)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Ввести площадь квартиры',
                callback_data=flat_selection_cd.new(building_name=building_name, option='flat_area')
            ),
            InlineKeyboardButton(
                text='Ввести цену квартиры',
                callback_data=flat_selection_cd.new(building_name=building_name, option='flat_price')
            )
        ],
        [
            InlineKeyboardButton(
                text='Год сдачи объекта',
                callback_data=flat_selection_cd.new(building_name=building_name, option='flat_year')
            ),
            InlineKeyboardButton(
                text='Количество комнат',
                callback_data=flat_selection_cd.new(building_name=building_name, option='flat_rooms')
            )
        ],
        [
            InlineKeyboardButton(
                text='Показать предложения',
                callback_data=show_flat_cd.new(building_name=building_name, option='show_flats')
            )
        ]
    ]

    markup.row(await menu_button(building_name))

    return markup


async def type_value_keyboard(building_name: str):
    """Создаем клавиатуру для ввода значения."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Рассматриваю все варианты',
                callback_data=flat_params.new(building_name=building_name, param=0),
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться',
                callback_data=building.new(name=building_name, section='flats'),
            )
        ],
    ]
    return markup


async def order_flats_keyboard(building_name: str):
    """Создаем клавиатуру с предложением показать квартиры в нужном порядке."""
    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='По возрастанию цены',
                callback_data=order_cd.new(building_name=building_name, sort='price_low_to_high'),
            )
        ],
        [
            InlineKeyboardButton(
                text='По убыванию цены',
                callback_data=order_cd.new(building_name=building_name, sort='price_high_to_low'),
            )
        ],
        [
            InlineKeyboardButton(
                text='По возрастанию площади',
                callback_data=order_cd.new(building_name=building_name, sort='area_low_to_high'),
            )
        ],
        [
            InlineKeyboardButton(
                text='По убыванию площади',
                callback_data=order_cd.new(building_name=building_name, sort='area_high_to_low'),
            )
        ],
        [
            InlineKeyboardButton(
                text='Вернуться',
                callback_data=building.new(name=building_name, section='flats')
            )
        ]
    ]
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
