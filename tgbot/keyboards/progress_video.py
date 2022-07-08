from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.about_project import project_cd
from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button


async def video_progress_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Выводим видео."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=project_cd.new(name=building_name, section='photo_gallery')
        )
    )

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
