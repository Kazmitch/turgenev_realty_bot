from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button

pagination_call = CallbackData("paginator", "key", "page")
# show_item = CallbackData("show_item", "item_id")


async def get_page_keyboard(max_pages: int, building_name: str, key="flat", page: int = 1):
    # Клавиатура будет выглядеть вот так:
    # |<< | <5> | >>|

    previous_page = page - 1
    previous_page_text = "<< "

    current_page_text = f"{page} из {max_pages}"

    next_page = page + 1
    next_page_text = " >>"

    markup = InlineKeyboardMarkup()
    if previous_page > 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key, page=previous_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_call.new(key=key, page="current_page")
        )
    )

    if next_page < max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key, page=next_page)
            )
        )
    markup.row(
        InlineKeyboardButton(
            text='Заказать обратный звонок',
            callback_data='contact'
        )
    )
    markup.row(await menu_button(building_name))

    return markup