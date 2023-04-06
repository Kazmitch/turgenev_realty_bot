from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

count_rooms_cd = CallbackData('count_rooms', 'building_name')
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


async def count_rooms_or_skip(building_name: str):
    callback_data = contact_cd.new(building_name=building_name)
    request_contact_button = InlineKeyboardButton(text="🟤 Пропустить",
                                                  callback_data=callback_data)
    return request_contact_button


async def contact_button(building_name: str):
    callback_data = count_rooms_cd.new(building_name=building_name)
    personal_offer = InlineKeyboardButton(text="🟤 Получить персональное предложение",
                                                  callback_data=callback_data)
    return personal_offer
