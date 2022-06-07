from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button
from tgbot.keyboards.send_contact import contact_button

project_cd = CallbackData('project', 'name', 'section')
photo_gallery_cd = CallbackData('photo_gallery', 'name', 'section')


async def about_project_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'О проекте'."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Фотогалерея',
                callback_data=project_cd.new(name=building_name, section='photo_gallery')
            )
        ]
    ]

    markup.row(await menu_button(building_name))

    return markup


async def photo_gallery_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Фотогалерея'."""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Расположение ЖК и инфраструктура',
                callback_data=photo_gallery_cd.new(name=building_name, section='location')
            )
        ],
        [
            InlineKeyboardButton(
                text='Строящиеся корпуса',
                callback_data=photo_gallery_cd.new(name=building_name, section='buildings_construction')
            )
        ],
        [
            InlineKeyboardButton(
                text='Интерьеры общих зон',
                callback_data=photo_gallery_cd.new(name=building_name, section='local_interiors')
            )
        ],
        [
            InlineKeyboardButton(
                text='Шоурум',
                callback_data=photo_gallery_cd.new(name=building_name, section='showroom')
            )
        ],
        [
            InlineKeyboardButton(
                text='Ход строительства live',
                callback_data=photo_gallery_cd.new(name=building_name, section='progress_live')
            )
        ],
        [
            InlineKeyboardButton(
                text='Аэрофотосъемка 3D',
                callback_data=photo_gallery_cd.new(name=building_name, section='photography_3d')
            )
        ]
    ]

    markup.row(await menu_button(building_name))

    return markup


async def photos_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Отображаем фотографии выбранной категории."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=project_cd.new(name=building_name, section='photo_gallery')
        )
    )

    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
