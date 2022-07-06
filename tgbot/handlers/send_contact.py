from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, ContentType

from realty_bot.realty_bot.comagic_api import make_call_request
from tgbot.keyboards.building_menu import menu_markup
from tgbot.keyboards.send_contact import contact, contact_cd
from tgbot.states.send_contact import ContactStates
from tgbot.utils.dp_api.db_commands import create_requests, create_comagic_call_request


async def send_contact(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    building_name = callback_data.get('building_name')
    await state.update_data(building_name=building_name)
    await call.message.answer(text=f'Оставьте номер, мы свяжемся с вами и предложим варианты квартир под ваш запрос.\n'
                                   f'Нажмите кнопку «Отправить контакт» или введите номер вручную',
                              reply_markup=contact)
    await call.message.delete()
    await ContactStates.contact.set()


async def get_contact(message: Message, state: FSMContext):
    if message.contact:
        await state.update_data(contact_user=message.contact.phone_number)
        phone_number = message.contact.phone_number
    else:
        await state.update_data(contact_user=message.text)
        phone_number = message.text
    data = await state.get_data()
    building_name = data.get('building_name')
    await state.finish()
    markup = await menu_markup(building_name)
    call = await create_comagic_call_request(building_name=building_name, site_id='69669')
    await message.answer(text='Готово, вы великолепны!', reply_markup=ReplyKeyboardRemove())
    await message.answer(text='Вы можете вернуться в главное меню', reply_markup=markup)
    await create_requests(building_name, message.from_user.id, phone_number, data)
    await make_call_request(call.api_token.access_token, data, site_id='69669')


def register_send_contact(dp: Dispatcher):
    dp.register_callback_query_handler(send_contact, contact_cd.filter(), state='*')
    dp.register_message_handler(get_contact, content_types=[ContentType.CONTACT, ContentType.TEXT],
                                state=ContactStates.contact)
