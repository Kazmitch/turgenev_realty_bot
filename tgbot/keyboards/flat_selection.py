from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с меню
from tgbot.keyboards.building_menu import main_building_menu

# flat_cd = CallbackData('flat_parameters', 'level', 'area', 'price', 'year', 'rooms', 'floor')
flat_cd = CallbackData('flat_parameters', 'level', 'area', 'price', 'year')


def make_callback_data(level, area='0', price='0', year='0', rooms='0', floor='0'):
    """
    Создаем коллбекдату для каждого элемента меню, в зависимости от передаваемых параметров.
    По умолчанию площадь, год, кол-во комнат
    """
    # return flat_cd.new(level=level, area=area, price=price, year=year, rooms=rooms, floor=floor)
    return flat_cd.new(level=level, area=area, price=price, year=year)


async def area_keyboard() -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором площади."""
    # Указываем, что текущий уровень меню - 0
    current_level = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    # Сформируем коллбек дату, которая будет на кнопке.
    callback_data = make_callback_data(level=current_level + 1)

    markup.insert(
        InlineKeyboardButton(text='Рассматриваю все варианты', callback_data=callback_data)
    )

    markup.row(main_building_menu)

    return markup


async def price_keyboard(area: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором цены."""
    # Указываем, что текущий уровень меню - 1
    current_level = 1

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    # Сформируем коллбек дату, которая будет на кнопке.
    callback_data = make_callback_data(level=current_level + 1, area=area)

    markup.insert(
        InlineKeyboardButton(text='Рассматриваю все варианты', callback_data=callback_data)
    )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=current_level - 1)
        )
    )
    markup.row(main_building_menu)

    return markup


async def year_keyboard() -> InlineKeyboardMarkup:
    """Создаем клавиатуру с выбором года."""
    # Указываем, что текущий уровень меню - 1
    current_level = 2

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    # # Сформируем коллбек дату, которая будет на кнопке.
    # callback_data = make_callback_data(level=current_level + 1)

    # markup.row(
    #     InlineKeyboardButton(
    #         text='Объект сдан',
    #         callback_data=make_callback_data(level=current_level + 1, year='в этом году')
    #     ),
    #     InlineKeyboardButton
    # )

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Объект сдан',
                callback_data=make_callback_data(level=current_level + 1, year='в этом году')
            ),
        ],
        [
            InlineKeyboardButton(
                text='До конца текущего года',
                callback_data=make_callback_data(level=current_level)
            )
        ]
    ]
