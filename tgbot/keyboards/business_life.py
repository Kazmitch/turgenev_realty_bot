from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button, contact_cd


async def business_life_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Апартаменты для бизнеса и жизни'."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='🎁 Получить персональное предложение',
                callback_data=contact_cd.new(building_name=building_name)
            )
        ]
    ]

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
