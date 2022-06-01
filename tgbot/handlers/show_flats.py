from aiogram import Dispatcher
from aiogram.types import CallbackQuery


async def show_flats(call: CallbackQuery, **kwargs):
    data = kwargs
    await call.message.answer("The best")


def register_show_flats(dp: Dispatcher):
    dp.register_callback_query_handler(show_flats, text='show_flats', state='*')
