from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.send_contact import contact_button
from tgbot.utils.dp_api.db_commands import get_documents


documentation_cd = CallbackData("document", "name", "document_id")


async def documents_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Документация'."""
    markup = InlineKeyboardMarkup(row_width=1)

    documents = await get_documents(building_name)

    for document in documents:
        button_text = document.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=documentation_cd.new(name=building_name, document_id=document.id)
            )
        )

    markup.row(await menu_button(building_name))

    return markup


async def current_declaration_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру под документацию."""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=building.new(name=building_name, section='documents')
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
