from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

purchase_terms_cd = CallbackData('terms', 'building_name', 'section', 'term')


async def purchase_terms_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Условия оплаты'."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def term_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Выводим условие."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=building.new(name=building_name, section='purchase_terms')
        )
    )

    markup.row(await call_button(building_name))
    # markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
