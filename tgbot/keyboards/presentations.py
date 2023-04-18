from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button
from tgbot.utils.dp_api.db_commands import get_about_project_presentations

project_cd = CallbackData('project', 'building_name', 'section')
photo_gallery_cd = CallbackData('photo_gallery', 'building_name', 'section')
presentation_cd = CallbackData('presentation', 'building_name', 'pres_id')


async def presentation_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'О проекте'."""
    markup = InlineKeyboardMarkup(row_width=2)

    presentations = await get_about_project_presentations(building_name)

    for presentation in presentations:
        button_text = presentation.title

        markup.row(
            InlineKeyboardButton(
                text=button_text,
                callback_data=presentation_cd.new(building_name=building_name, pres_id=presentation.id)
            )
        )

    markup.insert(await call_button(building_name))
    markup.insert(await contact_button(building_name))
    markup.insert(await menu_button(building_name))

    return markup
