from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


contact_cd = CallbackData('contact', 'building_name')

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отправить контакт', request_contact=True),
        ],
        [
            KeyboardButton(text='В начало')
        ]

    ],
    resize_keyboard=True
)


async def contact_button(building_name: str):
    callback_data = contact_cd.new(building_name=building_name)
    request_contact_button = InlineKeyboardButton(text="📞 Заказать обратный звонок", callback_data=callback_data)
    return request_contact_button
