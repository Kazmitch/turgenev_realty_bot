from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button


async def current_presentation_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для презентации."""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text='🟤 Вернуться',
            callback_data=building.new(name=building_name, section='project')
        )
    )

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
