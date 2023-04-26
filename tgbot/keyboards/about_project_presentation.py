from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button


async def current_presentation_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для презентации."""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(await call_button(building_name))
    markup.insert(await contact_button(building_name))
    markup.row(
        InlineKeyboardButton(
            text='🟫 Вернуться',
            callback_data=building.new(name=building_name, section='presentations')
        )
    )

    markup.insert(await menu_button(building_name))

    return markup
