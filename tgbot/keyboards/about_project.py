from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building, special_offer_button
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

project_cd = CallbackData('project', 'building_name', 'section')
photo_gallery_cd = CallbackData('photo_gallery', 'building_name', 'section')


async def about_project_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'О проекте'."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(await special_offer_button(building_name))

    markup.row(await call_button(building_name))
    # markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def photo_gallery_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Фотогалерея'."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='📍 Расположение ЖК и инфраструктура',
                callback_data=photo_gallery_cd.new(building_name=building_name, section='location')
            )
        ],
        [
            InlineKeyboardButton(
                text='🧱 Строящиеся корпуса',
                callback_data=photo_gallery_cd.new(building_name=building_name, section='construction')
            )
        ],
        [
            InlineKeyboardButton(
                text='🏠 Интерьеры общих зон',
                callback_data=photo_gallery_cd.new(building_name=building_name, section='interior')
            )
        ],
        [
            InlineKeyboardButton(
                text='👀 Шоурум',
                callback_data=photo_gallery_cd.new(building_name=building_name, section='showroom')
            )
        ],
        [
            InlineKeyboardButton(
                text='🏗 Ход строительства (видео)',
                callback_data=photo_gallery_cd.new(building_name=building_name, section='progress_video')
            )
        ]
    ]

    markup.row(await menu_button(building_name))

    return markup
