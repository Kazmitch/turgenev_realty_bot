from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.about_project import about_project_keyboard, project_cd, photo_gallery_keyboard, photos_keyboard, \
    photo_gallery_cd
from tgbot.keyboards.building_menu import building
from tgbot.states.send_contact import ContactStates
from tgbot.utils.dp_api.db_commands import get_developer_description


async def project(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'О проекте'"""
    building_name = callback_data.get('name')
    description = await get_developer_description(building_name)
    photo = open('content/photos/arbat_stars_project.jpg', 'rb')
    markup = await about_project_keyboard(building_name)
    await call.message.answer_photo(photo=photo,
                                    caption=description,
                                    reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def photo_gallery(call: CallbackQuery, callback_data: dict):
    """Хендлер на кнопку 'Фотогалерея'"""
    building_name = callback_data.get('name')
    markup = await photo_gallery_keyboard(building_name)
    await call.message.answer(text='Что хотели бы посмотреть?', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_photos(call: CallbackQuery, callback_data: dict):
    """Хендлер на отображение фотографий конкретной категории."""
    building_name = callback_data.get('name')
    section = callback_data.get('section')
    markup = await photos_keyboard(building_name)
    await call.message.answer(text='Давай посмотрим', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    await ContactStates.building_name.set()


def register_about_project(dp: Dispatcher):
    dp.register_callback_query_handler(project, building.filter(section='project'), state='*')
    dp.register_callback_query_handler(photo_gallery, project_cd.filter(section='photo_gallery'), state='*')
    dp.register_callback_query_handler(show_photos, photo_gallery_cd.filter(), state='*')
