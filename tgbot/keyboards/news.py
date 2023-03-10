from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

pagination_news_call = CallbackData("paginator_news", "building_name", "key", "page")


async def get_news_page_keyboard(max_pages: int, building_name: str, key="news", page: int = 1):
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
                callback_data=pagination_news_call.new(building_name=building_name, key=key, page=previous_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_news_call.new(building_name=building_name, key=key, page="current_page")
        )
    )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_news_call.new(building_name=building_name, key=key, page=next_page)
            )
        )
    markup.row(await call_button(building_name))
    # markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
