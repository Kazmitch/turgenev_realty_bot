from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, ContentType, InputFile

from realty_bot.realty_bot.calltouch_api import make_calltouch_call_request, make_calltouch_callback_request
from realty_bot.realty_bot.comagic_api import make_comagic_call_request
from realty_bot.realty_bot.settings import MEDIA_ROOT
from realty_bot.realty_bot.utils import correct_phone
from tgbot.keyboards.building_menu import menu_markup
from tgbot.keyboards.send_contact import contact, contact_cd, count_rooms_cd, count_rooms_or_skip
from tgbot.states.count_rooms import CountRoomsStates
from tgbot.states.send_contact import ContactStates
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import create_requests, get_userbot, get_personal_offer_photo
from tgbot.utils.dp_api.db_commands import get_call_request


async def write_rooms_count(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Хендлер на кнопку 'Получить персональное предложение'."""
    await call.answer(cache_time=60)
    building_name = callback_data.get('building_name')
    await state.update_data(building_name=building_name)
    markup = await count_rooms_or_skip(building_name)
    await call.message.answer(text='Укажите желаемое количество комнат. Можете написать или пропустить этот шаг.',
                              reply_markup=markup)
    await call.message.delete()
    await CountRoomsStates.count.set()
    await log_stat(call.from_user, event='Нажатие кнопки "Обратный звонок"')
    await insert_dict(call.from_user, event='Нажатие кнопки "Обратный звонок"')


async def send_contact(message: Union[CallbackQuery, Message], state: FSMContext, callback_data: dict = None):
    """Хендлер на кнопку 'Заказать обратный звонок'."""
    if isinstance(message, CallbackQuery):
        call = message
        await call.answer(cache_time=60)
        building_name = callback_data.get('building_name')
        await state.update_data(building_name=building_name)
        photo = await get_personal_offer_photo(building_name)
        file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
        msg = await call.message.answer_photo(
            photo=file,
            caption=f'Получите персональное предложение в офисе продаж TURGENEV!\n'
                    f'Оставьте номер, мы свяжемся с вами и предложим варианты квартир под ваш запрос.\n'
                    f'Нажмите кнопку «Отправить контакт» или введите номер вручную, в формате <b>79091234567</b>',
            reply_markup=contact)
        await state.update_data(msg_id=msg.message_id)
        await call.message.delete()
        await ContactStates.contact.set()
        await log_stat(call.from_user, event='Ввод количества комнат')
        await insert_dict(call.from_user, event='Ввод количества комнат')
    else:
        data = await state.get_data()
        rooms_text = message.text
        building_name = data.get('building_name')
        await state.update_data(rooms_count=rooms_text)
        photo = await get_personal_offer_photo(building_name)
        file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{photo.photo.name}')
        msg = await message.answer_photo(
            photo=file,
            caption=f'Получите персональное предложение в офисе продаж TURGENEV!\n'
                    f'Оставьте номер, мы свяжемся с вами и предложим варианты квартир под ваш запрос.\n'
                    f'Нажмите кнопку «Отправить контакт» или введите номер вручную, в формате <b>79091234567</b>',
            reply_markup=contact)
        await state.update_data(msg_id=msg.message_id)
        await ContactStates.contact.set()
        await log_stat(message.from_user, event='Ввод количества комнат')
        await insert_dict(message.from_user, event='Ввод количества комнат')


async def get_contact(message: Message, state: FSMContext):
    """Хендлер на кнопку 'Отправить контакт'."""
    data = await state.get_data()
    building_name = data.get('building_name')
    markup = await menu_markup(building_name)
    if message.contact:
        await state.update_data(contact_user=message.contact.phone_number, telegram_id=message.from_user.id)
        phone = message.contact.phone_number
        phone_number = ''.join(e for e in phone if e.isdigit())
    else:
        await state.update_data(contact_user=message.text, telegram_id=message.from_user.id)
        phone = message.text
        phone_number = correct_phone(phone)
    if phone_number:
        data = await state.get_data()
        await state.finish()
        user = await get_userbot(message.from_user.id)
        calltracking = user.calltracking
        source = user.get_source
        source_id = user.get_source_id
        telegram_first_name = message.from_user.first_name
        if calltracking == 'comagic':
            call = await get_call_request(building_name=building_name, **{source: source_id.get(source)})
            call_request = await make_comagic_call_request(call.api_token.access_token, name=telegram_first_name,
                                                           phone_number=phone_number,
                                                           data=data, source=source, source_id=source_id.get(source))
            if call_request:
                await message.answer(text='Готово, вы великолепны!', reply_markup=ReplyKeyboardRemove())
                await message.answer(text='Вы можете вернуться в главное меню', reply_markup=markup)
                await create_requests(building_name, message.from_user.id, phone_number, data)
                await log_stat(message.from_user, event=f'Отправили контакт в Comagic с {source_id}')
                await insert_dict(message.from_user, event=f'Отправили контакт в Comagic с {source_id}',
                                  phone_number=phone_number)
            else:
                await message.answer(text='Упс(', reply_markup=ReplyKeyboardRemove())
                await message.answer(text="Что-то пошло не так, попробуйте еще раз.", reply_markup=markup)
        elif calltracking == 'calltouch':
            call = await get_call_request(building_name=building_name, site_id=source_id.get('site_id'),
                                          campaign_id=source_id.get('campaign_id'))
            if call.route_key:
                call_request = await make_calltouch_callback_request(call.api_token.access_token,
                                                                     name=telegram_first_name,
                                                                     route_key=call.route_key,
                                                                     source=call.campaign_id,
                                                                     phone_number=phone_number,
                                                                     data=data)
            else:
                call_request = await make_calltouch_call_request(call.api_token.access_token,
                                                                 site_id=source_id.get('site_id'),
                                                                 source=call.campaign_id,
                                                                 name=telegram_first_name,
                                                                 phone_number=phone_number, data=data)
            if call_request:
                await message.answer(text='Готово, вы великолепны!', reply_markup=ReplyKeyboardRemove())
                await message.answer(text='Вы можете вернуться в главное меню', reply_markup=markup)
                await create_requests(building_name, message.from_user.id, phone_number, data)
                await log_stat(message.from_user, event=f'Отправили контакт в Calltouch с {source_id}')
                await insert_dict(message.from_user, event=f'Отправили контакт в Calltouch с {source_id}',
                                  phone_number=phone_number)
            else:
                await message.answer(text='Упс(', reply_markup=ReplyKeyboardRemove())
                await message.answer(text="Что-то пошло не так, попробуйте еще раз.", reply_markup=markup)

    else:
        await message.answer(text="Вы ввели неправильный номер", reply_markup=markup)
        await log_stat(message.from_user, error='Ввели неправильный номер')
        await insert_dict(message.from_user, error='Ввели неправильный номер')


def register_send_contact(dp: Dispatcher):
    dp.register_callback_query_handler(write_rooms_count, count_rooms_cd.filter(), state='*')
    dp.register_callback_query_handler(send_contact, contact_cd.filter(), state=CountRoomsStates.count)
    dp.register_message_handler(send_contact, state=CountRoomsStates.count)
    dp.register_message_handler(get_contact, content_types=[ContentType.CONTACT, ContentType.TEXT],
                                state=ContactStates.contact)
