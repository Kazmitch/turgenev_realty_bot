from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button


async def business_life_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Апартаменты для бизнеса и жизни'."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
