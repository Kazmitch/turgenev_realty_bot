from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.dynamics import pagination_construction_call, get_construction_page_keyboard
from tgbot.utils.dp_api.db_commands import get_construction_photos
from tgbot.utils.page import get_page


async def show_construction(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Динамика строительства'"""
    building_name = callback_data.get('name')
    constructs = await get_construction_photos(building_name)
    max_constructs = len(constructs)
    construction = await get_page(constructs)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{construction.photo.name}')
    await call.message.answer_photo(
        photo=file,
        caption=f'Дата: {construction.photo_date.strftime("%d.%m.%Y")}',
        reply_markup=await get_construction_page_keyboard(
            max_pages=max_constructs,
            building_name=building_name,
            key='constructing'
        )
    )
    await call.message.delete()


async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


async def show_chosen_construction(call: CallbackQuery, callback_data: dict, **kwargs):
    """Отображаем выбранную страницу."""
    building_name = callback_data.get('building_name')
    current_page = int(callback_data.get('page'))
    constructs = await get_construction_photos(building_name)
    max_constructs = len(constructs)
    construction = await get_page(constructs, page=current_page)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{construction.photo.name}')
    media = InputMediaPhoto(media=file,
                            caption=f'Дата: {construction.photo_date.strftime("%d.%m.%Y")}')
    await call.message.edit_media(
        media=media,
        reply_markup=await get_construction_page_keyboard(
            max_pages=max_constructs,
            building_name=building_name,
            key='constructing',
            page=current_page
        )
    )


def register_construction(dp: Dispatcher):
    dp.register_callback_query_handler(show_construction, building.filter(section='construction'), state='*')
    dp.register_callback_query_handler(current_page_error, pagination_construction_call.filter(page='current_page'))
    dp.register_callback_query_handler(show_chosen_construction,
                                       pagination_construction_call.filter(key='constructing'), state='*')
