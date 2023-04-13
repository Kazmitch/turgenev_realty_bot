from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

pagination_flats_call = CallbackData("paginator_flats", "key", "page", "sort", "rooms")


async def get_page_keyboard(max_pages: int, building_name: str, sort: str, rooms: str, key="flat", page: int = 1):
    # Клавиатура будет выглядеть вот так:
    # |<< | <5> | >>|

    previous_page = page - 1
    previous_page_text = "⬅ "

    current_page_text = f"{page} из {max_pages}"

    next_page = page + 1
    next_page_text = " ➡"

    markup = InlineKeyboardMarkup()
    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_flats_call.new(key=key, page=previous_page, sort=sort, rooms=rooms)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_flats_call.new(key=key, page="current_page", sort=sort, rooms=rooms)
        )
    )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_flats_call.new(key=key, page=next_page, sort=sort, rooms=rooms)
            )
        )
    markup.row(await call_button(building_name))
    markup.row(
        InlineKeyboardButton(
            text='🟫 Вернуться',
            callback_data=building.new(name=building_name, section='flats')
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
