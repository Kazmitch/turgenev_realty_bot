from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputFile

from tgbot.keyboards.flat_pagination import get_page_keyboard, pagination_flats_call
from tgbot.keyboards.flat_selection import order_cd
from tgbot.keyboards.send_contact import contact_markup
from tgbot.states.send_contact import ContactStates
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_xml_link_by_name
from tgbot.utils.images import resize_photo
from tgbot.utils.offers import get_offers, get_photo_url, get_values
from tgbot.utils.page import get_page


async def show_chosen_flats(call: CallbackQuery, state: FSMContext, callback_data: dict, **kwargs):
    data = await state.get_data()
    building_name = data.get('building_name')
    ordering = callback_data.get('sort')
    flat_params = data.get('params')
    offers = await get_offers(building_name, flat_params, ordering)
    xml_link = await get_xml_link_by_name(building_name)
    if offers:
        max_pages = len(offers)
        offer = await get_page(offers)
        try:
            photo_url = await get_photo_url(offer, xml_link.type_of_xml)
            photo = await resize_photo(photo_url)
        except KeyError:
            photo = 'realty_bot/media/errors/layout_error.jpg'
        file = InputFile(path_or_bytesio=photo)
        offer_values = await get_values(offer, xml_link.type_of_xml)
        price = f'{int(offer_values.get("offer_price").split(".")[0]):_}'.replace('_', ' ')
        await call.message.answer_photo(
            photo=file,
            caption=f'Стоимость: <b>{price} руб.</b>\n'
                    f'Площадь: <b>{offer_values.get("offer_area")} м²</b>\n'
                    f'Комнат: <b>{offer_values.get("offer_rooms") if offer_values.get("offer_rooms") else "Не указано"}</b>\n'
                    f'Этаж: <b>{offer_values.get("offer_floor")}</b>',
            reply_markup=await get_page_keyboard(
                key='flat',
                max_pages=max_pages,
                building_name=building_name,
                sort=ordering
            )
        )
        await call.message.delete()
        await ContactStates.building_name.set()
        await log_stat(call.from_user, event='Просмотр квартир')
        await insert_dict(call.from_user, event='Просмотр квартир')
        await state.update_data(current_flat={'price': offer_values.get("offer_price"),
                                              'area': offer_values.get("offer_area"),
                                              'rooms': offer_values.get("offer_rooms"),
                                              'floor': offer_values.get("offer_floor")})

    else:
        markup = await contact_markup(building_name)
        await call.message.answer(text='К сожалению, не смогли найти квартиры по данным параметрам.\n'
                                       'Давайте поможем вам подобрать', reply_markup=markup)
        await call.message.delete()
        await ContactStates.building_name.set()


async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)
    await log_stat(call.from_user, error='Нажатие на текущую страницу при листании квартир')


async def show_chosen_page(call: CallbackQuery, state: FSMContext, callback_data: dict, **kwargs):
    data = await state.get_data()
    building_name = data.get('building_name')
    ordering = callback_data.get('sort')
    flat_params = data.get('params')
    offers = await get_offers(building_name, flat_params, ordering)
    current_page = int(callback_data.get('page'))
    offer = await get_page(offers, page=current_page)
    xml_link = await get_xml_link_by_name(building_name)
    offer_values = await get_values(offer, xml_link.type_of_xml)
    price = f'{int(offer_values.get("offer_price").split(".")[0]):_}'.replace('_', ' ')
    try:
        photo_url = await get_photo_url(offer, xml_link.type_of_xml)
        photo = await resize_photo(photo_url)
    except KeyError:
        photo = 'realty_bot/media/errors/layout_error.jpg'
    file = InputFile(path_or_bytesio=photo)
    media = InputMediaPhoto(media=file,
                            caption=f'Стоимость: <b>{price} руб.</b>\n'
                                    f'Площадь: <b>{offer_values.get("offer_area")} м²</b>\n'
                                    f'Комнат: <b>{offer_values.get("offer_rooms") if offer_values.get("offer_rooms") else "Не указано"}</b>\n'
                                    f'Этаж: <b>{offer_values.get("offer_floor")}</b>')
    max_pages = len(offers)
    await call.message.edit_media(
        media=media,
        reply_markup=await get_page_keyboard(
            building_name=building_name,
            key='flat',
            max_pages=max_pages,
            page=current_page,
            sort=ordering
        )
    )
    await ContactStates.building_name.set()
    await state.update_data(current_flat={'price': offer_values.get("offer_price"),
                                          'area': offer_values.get("offer_area"),
                                          'rooms': offer_values.get("offer_rooms"),
                                          'floor': offer_values.get("offer_floor")})
    await log_stat(call.from_user, event='Листание квартир')
    await insert_dict(call.from_user, event='Листание квартир')


def register_show_flats(dp: Dispatcher):
    dp.register_callback_query_handler(show_chosen_flats, order_cd.filter(), state='*')
    dp.register_callback_query_handler(current_page_error, pagination_flats_call.filter(page='current_page'), state='*')
    dp.register_callback_query_handler(show_chosen_page, pagination_flats_call.filter(key='flat'), state='*')
