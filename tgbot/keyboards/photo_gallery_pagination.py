from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.about_project import project_cd, photo_gallery_cd
from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

pagination_gallery_call = CallbackData("paginator_gallery", "key", "page", "building_name", "section")
pagination_corpus = CallbackData("paginator_corpus", "key", "page", "building_name", "section", "corpus_id")


async def get_photos_keyboard(max_pages: int, building_name: str, section, key="photo",
                              page: int = 1) -> InlineKeyboardMarkup:
    """Отображаем фотографии выбранной категории."""

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
                callback_data=pagination_gallery_call.new(key=key, page=previous_page, building_name=building_name,
                                                          section=section)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_gallery_call.new(key=key, page="current_page", building_name=building_name,
                                                      section=section)
        )
    )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_gallery_call.new(key=key, page=next_page, building_name=building_name,
                                                          section=section)
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=project_cd.new(building_name=building_name, section='photo_gallery')
        )
    )

    markup.row(await call_button(building_name))
    # markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def get_corpus_photos_keyboard(max_pages: int, building_name: str, section, corpus_id: int, key="corpus",
                                     page: int = 1) -> InlineKeyboardMarkup:
    """Отображаем фотографии выбранного корпуса."""

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
                callback_data=pagination_corpus.new(key=key, page=previous_page, building_name=building_name,
                                                    section=section, corpus_id=corpus_id)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=current_page_text,
            callback_data=pagination_corpus.new(key=key, page="current_page", building_name=building_name,
                                                section=section, corpus_id=corpus_id)
        )
    )

    if next_page <= max_pages:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_corpus.new(key=key, page=next_page, building_name=building_name,
                                                    section=section, corpus_id=corpus_id)
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=photo_gallery_cd.new(building_name=building_name, section='construction')
        )
    )

    markup.row(await call_button(building_name))
    # markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
