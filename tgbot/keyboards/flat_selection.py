from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с меню
from tgbot.keyboards.building_menu import main_building_menu, menu_button

# flat_cd = CallbackData('flat_parameters', 'level', 'area', 'price', 'year', 'rooms', 'floor')
flat_cd = CallbackData('flat_parameters', 'building_name', 'level', 'area', 'price', 'year', 'rooms', 'floor')


def make_callback_data(building_name, level, area='0', price='0', year='0', rooms='0', floor='0'):
    """
    Создаем коллбекдату для каждого элемента меню, в зависимости от передаваемых параметров.
    По умолчанию площадь, год, кол-во комнат
    """
    # return flat_cd.new(level=level, area=area, price=price, year=year, rooms=rooms, floor=floor)
    return flat_cd.new(building_name=building_name, level=level, area=area, price=price, year=year, rooms=rooms, floor=floor)


async def area_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором площади."""
    # Указываем, что текущий уровень меню - 0
    current_level = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    # Сформируем коллбек дату, которая будет на кнопке.
    callback_data = make_callback_data(level=current_level + 1, building_name=building_name)

    markup.insert(
        InlineKeyboardButton(text='Рассматриваю все варианты', callback_data=callback_data)
    )

    markup.row(await menu_button(building_name))

    return markup


async def price_keyboard(area: str, building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором цены."""
    # Указываем, что текущий уровень меню - 1
    current_level = 1

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    # Сформируем коллбек дату, которая будет на кнопке.
    callback_data = make_callback_data(level=current_level + 1, building_name=building_name, area=area)

    markup.insert(
        InlineKeyboardButton(text='Рассматриваю все варианты', callback_data=callback_data)
    )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=current_level - 1, building_name=building_name)
        )
    )
    markup.row(await menu_button(building_name))

    return markup


async def year_keyboard(area: str, price: str, building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором года."""
    # Указываем, что текущий уровень меню - 2
    current_level = 2

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Объект сдан',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year='ho')
            ),
        ],
        [
            InlineKeyboardButton(
                text='До конца текущего года',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year='ty')
            )
        ],
        [
            InlineKeyboardButton(
                text='Рассматриваю все варианты',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price)
            )
        ]
    ]

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=current_level - 1, building_name=building_name, area=area)
        )
    )
    markup.row(await menu_button(building_name))

    return markup


async def rooms_keyboard(area: str, price: str, year: str, building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором кол-ва комнат."""
    # Указываем, что текущий уровень меню - 3
    current_level = 3

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Студия/1 комната',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year=year,
                                                 rooms='s/1')
            ),
        ],
        [
            InlineKeyboardButton(
                text='2 комнаты',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year=year,
                                                 rooms='2r')
            )
        ],
        [
            InlineKeyboardButton(
                text='3 и более',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year=year,
                                                 rooms='3m')
            )
        ],
        [
            InlineKeyboardButton(
                text='Рассматриваю все варианты',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price)
            )
        ]
    ]

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=current_level - 1, building_name=building_name, area=area, price=price)
        )
    )
    markup.row(await menu_button(building_name))

    return markup


async def floor_keyboard(area: str, price: str, year: str, rooms: str, building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором этажа."""

    # Указываем, что текущий уровень меню - 4
    current_level = 4

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Не 1-й этаж',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year=year,
                                                 rooms=rooms, floor='no1')
            ),
        ],
        [
            InlineKeyboardButton(
                text='Не последний этаж',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year=year,
                                                 rooms=rooms, floor='no_la')
            )
        ],
        [
            InlineKeyboardButton(
                text='Рассматриваю все варианты',
                callback_data=make_callback_data(level=current_level + 1, building_name=building_name, area=area, price=price, year=year,
                                                 rooms=rooms)
            )
        ]
    ]

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=current_level - 1, building_name=building_name, area=area, price=price, year=year)
        )
    )
    markup.row(await menu_button(building_name))

    return markup
