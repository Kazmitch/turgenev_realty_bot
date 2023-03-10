from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

flat_selection_cd = CallbackData('selection', 'building_name', 'option')


async def flat_selection_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Подобрать квартиру'."""

    markup = InlineKeyboardMarkup(row_width=2)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='1 спальня',
                callback_data=flat_selection_cd.new(building_name=building_name, option='1')
            ),
            InlineKeyboardButton(
                text='2 спальни',
                callback_data=flat_selection_cd.new(building_name=building_name, option='2')
            )
        ],
        [
            InlineKeyboardButton(
                text='3 спальни и более',
                callback_data=flat_selection_cd.new(building_name=building_name, option='3')
            ),
            InlineKeyboardButton(
                text='Пентхаусы',
                callback_data=flat_selection_cd.new(building_name=building_name, option='5')
            )
        ]
    ]

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
