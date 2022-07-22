from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.news import get_news_page_keyboard, pagination_news_call
from tgbot.utils.analytics import log_stat
from tgbot.utils.dp_api.db_commands import get_news
from tgbot.utils.news_text import make_news_text
from tgbot.utils.page import get_page


async def show_news(call: CallbackQuery, callback_data: dict, state: FSMContext, influx_client, **kwargs):
    """Хендлер на кнопку 'Новости'"""
    building_name = callback_data.get('name')
    news = await get_news(building_name)
    max_news = len(news)
    piece_of_news = await get_page(news)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{piece_of_news.photo.name}')
    text = await make_news_text(piece_of_news)
    await call.message.answer_photo(
        photo=file,
        caption=text,
        reply_markup=await get_news_page_keyboard(
            max_pages=max_news,
            building_name=building_name,
            key='news'
        )
    )
    await call.message.delete()
    await state.update_data(section=callback_data.get('section'))
    await log_stat(influx_client, call.from_user, call.message.date, event='Нажатие кнопки "Новости"')


async def current_page_error(call: CallbackQuery, influx_client):
    await call.answer(cache_time=60)
    await log_stat(influx_client, call.from_user, call.message.date,
                   error='Нажатие на текущую страницу при листании новостей')


async def show_chosen_news(call: CallbackQuery, callback_data: dict, state: FSMContext, influx_client, **kwargs):
    """Отображаем выбранную страницу."""
    building_name = callback_data.get('building_name')
    current_page = int(callback_data.get('page'))
    news = await get_news(building_name)
    max_news = len(news)
    piece_of_news = await get_page(news, page=current_page)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{piece_of_news.photo.name}')
    text = await make_news_text(piece_of_news)
    media = InputMediaPhoto(media=file,
                            caption=text)
    await call.message.edit_media(
        media=media,
        reply_markup=await get_news_page_keyboard(
            max_pages=max_news,
            building_name=building_name,
            key='news',
            page=current_page
        )
    )
    await state.update_data(section=callback_data.get('section'))
    await log_stat(influx_client, call.from_user, call.message.date, event='Листание новостей')


def register_news(dp: Dispatcher):
    dp.register_callback_query_handler(show_news, building.filter(section='news'), state='*')
    dp.register_callback_query_handler(current_page_error, pagination_news_call.filter(page='current_page'))
    dp.register_callback_query_handler(show_chosen_news, pagination_news_call.filter(key='news'), state='*')
