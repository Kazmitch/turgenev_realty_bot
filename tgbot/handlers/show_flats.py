import io

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputFile

from tgbot.keyboards.flat_pagination import get_page_keyboard, pagination_flats_call
from tgbot.keyboards.flat_selection import order_cd
from tgbot.keyboards.send_contact import contact_markup
from tgbot.states.send_contact import ContactStates
from tgbot.utils.dp_api.db_commands import get_xml_link_by_name
from tgbot.utils.images import get_photo_bytes
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
            photo = io.BytesIO(await get_photo_bytes(photo_url))
        except KeyError:
            photo = 'realty_bot/media/errors/layout_error.jpg'
        file = InputFile(path_or_bytesio=photo)
        offer_values = await get_values(offer, xml_link.type_of_xml)
        await call.message.answer_photo(
            photo=file,
            caption=f'Стоимость: <b>{offer_values.get("offer_price")} рублей</b>\n'
                    f'Площадь: <b>{offer_values.get("offer_area")} м²</b>\n'
                    f'Комнат: <b>{offer_values.get("offer_rooms")}</b>\n'
                    f'Этаж: <b>{offer_values.get("offer_floor")}</b>',
            reply_markup=await get_page_keyboard(
                key='flat',
                max_pages=max_pages,
                building_name=building_name,
                sort=ordering
            )
        )
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.delete()
        await ContactStates.building_name.set()
    else:
        markup = await contact_markup(building_name)
        await call.message.answer(text='К сожалению, не смогли найти квартиры по данным параметрам.\n'
                                       'Давайте поможем вам подобрать', reply_markup=markup)
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.delete()
        await ContactStates.building_name.set()


async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


async def show_chosen_page(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    building_name = data.get('building_name')
    ordering = callback_data.get('sort')
    flat_params = data.get('params')
    offers = await get_offers(building_name, flat_params, ordering)
    current_page = int(callback_data.get('page'))
    offer = await get_page(offers, page=current_page)
    xml_link = await get_xml_link_by_name(building_name)
    offer_values = await get_values(offer, xml_link.type_of_xml)
    try:
        photo_url = await get_photo_url(offer, xml_link.type_of_xml)
        photo = io.BytesIO(await get_photo_bytes(photo_url))
    except KeyError:
        photo = 'realty_bot/media/errors/layout_error.jpg'
    file = InputFile(path_or_bytesio=photo)
    media = InputMediaPhoto(media=file,
                            caption=f'Стоимость: <b>{offer_values.get("offer_price")} рублей</b>\n'
                                    f'Площадь: <b>{offer_values.get("offer_area")} м²</b>\n'
                                    f'Комнат: <b>{offer_values.get("offer_rooms")}</b>\n'
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


def register_show_flats(dp: Dispatcher):
    dp.register_callback_query_handler(show_chosen_flats, order_cd.filter(), state='*')
    dp.register_callback_query_handler(current_page_error, pagination_flats_call.filter(page='current_page'))
    dp.register_callback_query_handler(show_chosen_page, pagination_flats_call.filter(key='flat'), state='*')
