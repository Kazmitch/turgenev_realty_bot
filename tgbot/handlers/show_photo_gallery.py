from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.about_project import photo_gallery_keyboard, project_cd, photo_gallery_cd
from tgbot.keyboards.photo_gallery_pagination import get_photos_keyboard, pagination_gallery_call
from tgbot.states.send_contact import ContactStates
from tgbot.utils.dp_api.db_commands import get_gallery_photos
from tgbot.utils.page import get_page


async def photo_gallery(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Хендлер на кнопку 'Фотогалерея'"""
    building_name = callback_data.get('name')
    markup = await photo_gallery_keyboard(building_name)
    await call.message.answer(text='Я вижу, тебе стало интересно! ☺ Ты можешь посмотреть на комплекс прямо тут! 👇',
                              reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_photos(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Хендлер на отображение фотографий конкретной категории."""
    building_name = callback_data.get('name')
    section = callback_data.get('section')
    photos = await get_gallery_photos(section, building_name)
    max_pages = len(photos)
    photo = await get_page(photos)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
    await call.message.answer_photo(
        photo=file,
        caption=photo.description,
        reply_markup=await get_photos_keyboard(
            max_pages=max_pages,
            key='photo',
            building_name=building_name,
            section=section
        )
    )
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    # await ContactStates.building_name.set()
    await state.update_data(section=callback_data.get('section'))


async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


async def show_chosen_page_photos(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Хендлер на отображение нужной страницы."""
    building_name = callback_data.get('name')
    section = callback_data.get('section')
    current_page = int(callback_data.get('page'))
    photos = await get_gallery_photos(section, building_name)
    max_pages = len(photos)
    photo = await get_page(photos, page=current_page)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
    media = InputMediaPhoto(media=file, caption=photo.description)
    await call.message.edit_media(
        media=media,
        reply_markup=await get_photos_keyboard(
            max_pages=max_pages,
            key='photo',
            building_name=building_name,
            section=section,
            page=current_page
        )
    )
    # await ContactStates.building_name.set()
    await state.update_data(section=callback_data.get('section'))


def register_show_gallery(dp: Dispatcher):
    dp.register_callback_query_handler(photo_gallery, project_cd.filter(section='photo_gallery'), state='*')
    dp.register_callback_query_handler(show_photos, photo_gallery_cd.filter(), state='*')
    dp.register_callback_query_handler(current_page_error, pagination_gallery_call.filter(page='current_page'))
    dp.register_callback_query_handler(show_chosen_page_photos, pagination_gallery_call.filter(key='photo'), state='*')
