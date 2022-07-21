from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.about_project import project_cd
from tgbot.keyboards.building_menu import menu_button
from tgbot.utils.dp_api.db_commands import get_corpuses

corpus_cd = CallbackData("corpus", "building_name", "section", "corpus_id")


async def corpuses_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Строящиеся корпуса'."""
    markup = InlineKeyboardMarkup(row_width=1)

    corpuses = await get_corpuses(building_name)

    for corpus in corpuses:
        button_text = corpus.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=corpus_cd.new(building_name=building_name, section="corpuses", corpus_id=corpus.id)
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=project_cd.new(building_name=building_name, section='photo_gallery')
        )
    )
    markup.row(await menu_button(building_name))

    return markup
