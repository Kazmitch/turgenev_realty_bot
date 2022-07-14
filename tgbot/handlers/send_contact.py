from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, ContentType

from realty_bot.realty_bot.comagic_api import make_call_request
from realty_bot.realty_bot.utils import correct_phone
from tgbot.keyboards.building_menu import menu_markup
from tgbot.keyboards.send_contact import contact, contact_cd
from tgbot.states.send_contact import ContactStates
from tgbot.utils.dp_api.db_commands import create_requests, create_comagic_call_request, get_userbot


async def send_contact(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    building_name = callback_data.get('building_name')
    await state.update_data(building_name=building_name)
    await call.message.answer(text=f'Оставьте номер, мы свяжемся с вами и предложим варианты квартир под ваш запрос.\n'
                                   f'Нажмите кнопку «Отправить контакт» или введите номер вручную, в формате <b>79091234567</b>',
                              reply_markup=contact)
    await call.message.delete()
    await ContactStates.contact.set()


async def get_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    building_name = data.get('building_name')
    markup = await menu_markup(building_name)
    if message.contact:
        await state.update_data(contact_user=message.contact.phone_number)
        phone = message.contact.phone_number
        phone_number = ''.join(e for e in phone if e.isdigit())
    else:
        await state.update_data(contact_user=message.text)
        phone = message.text
        phone_number = correct_phone(phone)
    if phone_number:
        data = await state.get_data()
        await state.finish()
        user = await get_userbot(message.from_user.id)
        source = user.get_source
        source_id = user.get_source_id
        telegram_first_name = message.from_user.first_name
        if source == 'site_id':
            call = await create_comagic_call_request(building_name=building_name, site_id=source_id)
            await make_call_request(call.api_token.access_token, name=telegram_first_name, phone_number=phone_number,
                                    data=data, source=source, source_id=source_id)
        elif source == 'campaign_id':
            call = await create_comagic_call_request(building_name=building_name, campaign_id=source_id)
            await make_call_request(call.api_token.access_token, name=telegram_first_name, phone_number=phone_number,
                                    data=data, source=source, source_id=source_id)
        await message.answer(text='Готово, вы великолепны!', reply_markup=ReplyKeyboardRemove())
        await message.answer(text='Вы можете вернуться в главное меню', reply_markup=markup)
        await create_requests(building_name, message.from_user.id, phone_number, data)

    else:
        await message.answer(text="Вы ввели неправильный номер", reply_markup=markup)


def register_send_contact(dp: Dispatcher):
    dp.register_callback_query_handler(send_contact, contact_cd.filter(), state='*')
    dp.register_message_handler(get_contact, content_types=[ContentType.CONTACT, ContentType.TEXT],
                                state=ContactStates.contact)
