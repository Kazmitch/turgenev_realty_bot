from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


call_cd = CallbackData('call', 'building_name')


async def call_button(building_name: str):
    callback_data = call_cd.new(building_name=building_name)
    call = InlineKeyboardButton(text="🟫 Позвонить в отдел продаж", callback_data=callback_data)
    return call
