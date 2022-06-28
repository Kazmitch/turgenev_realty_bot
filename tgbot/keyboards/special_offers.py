from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.send_contact import contact_button
from tgbot.utils.dp_api.db_commands import get_special_offers


special_offer_cd = CallbackData("offer", "name", "offer_id")


async def special_offers_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Спецпредложения'."""
    markup = InlineKeyboardMarkup(row_width=1)

    special_offers = await get_special_offers(building_name)

    for special_offer in special_offers:
        button_text = special_offer.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=special_offer_cd.new(name=building_name, offer_id=special_offer.id)
            )
        )

    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def current_offer_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру под спецпредложение."""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=building.new(name=building_name, section='offers')
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
