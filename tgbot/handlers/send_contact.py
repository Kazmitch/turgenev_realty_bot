from aiogram import Dispatcher

from tgbot.keyboards.send_contact import contact
from aiogram.types import CallbackQuery, InputMediaPhoto


async def send_contact(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer(text=f'Оставьте номер, мы свяжемся с вами и предложим варианты квартир под ваш запрос.\n'
                                   f'Нажмите кнопку «Отправить контакт» или введите номер вручную', reply_markup=contact)
    await call.message.delete()


def register_send_contact(dp: Dispatcher):
    dp.register_callback_query_handler(send_contact, text='contact', state='*')
