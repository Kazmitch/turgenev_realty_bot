from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMedia

from tgbot.keyboards.flat_pagination import get_page_keyboard, pagination_call
from tgbot.states.flat_selection import FlatStates
from tgbot.utils.dp_api.db_commands import get_xml_link_by_name
from tgbot.utils.images import make_photo, get_photo_bytes
from tgbot.utils.page import get_offer
from tgbot.utils.xml_to_dict import get_offers_yan


async def show_flats(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    building_name = data.get('building_name')
    area = data.get('area')
    price = data.get('price')
    year = data.get('year')
    rooms = data.get('rooms')
    floor = data.get('floor')
    xml_link = await get_xml_link_by_name(building_name)
    offers = await get_offers_yan(xml_link, area, price, year, rooms, floor)
    max_pages = len(offers)
    # offers_with_photo = await make_photo(offers)
    offer = await get_offer(offers)
    photo = await get_photo_bytes(offer['image'][0]['#text'])
    offer_area = offer['area']['value']
    offer_price = offer['price']['value']
    offer_description = offer['description']
    await call.message.answer_photo(
        photo=photo,
        caption=f'Стоимость: <b>{offer_price} рублей</b>\n'
                f'Площадь: <b>{offer_area} м²</b>\n',
        reply_markup=await get_page_keyboard(
            key='flat',
            max_pages=max_pages,
            building_name=building_name
        )
    )


async def current_page_error(call: CallbackQuery):
    await call.answer(cache_time=60)


async def show_chosen_page(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    building_name = data.get('building_name')
    area = data.get('area')
    price = data.get('price')
    year = data.get('year')
    rooms = data.get('rooms')
    floor = data.get('floor')
    xml_link = await get_xml_link_by_name(building_name)
    offers = await get_offers_yan(xml_link, area, price, year, rooms, floor)
    current_page = int(callback_data.get('page'))
    offer = await get_offer(offers, page=current_page)
    offer_area = offer['area']['value']
    offer_price = offer['price']['value']
    photo = await get_photo_bytes(offer['image'][0]['#text'])
    # photo = offer['image'][1]
    # media = InputMediaPhoto(media=photo,
    #                         caption=f'Стоимость: <b>{offer_price} рублей</b>\n'
    #                                 f'Площадь: <b>{offer_area} м²</b>\n', )
    max_pages = len(offers)
    await call.message.answer_photo(
        photo=photo,
        caption=f'Стоимость: <b>{offer_price} рублей</b>\n'
                f'Площадь: <b>{offer_area} м²</b>\n',
        reply_markup=await get_page_keyboard(
            building_name=building_name,
            key='flat',
            max_pages=max_pages,
            page=current_page
        )
    )
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


def register_show_flats(dp: Dispatcher):
    dp.register_callback_query_handler(show_flats, text='show_flats', state=FlatStates.flat_data)
    dp.register_callback_query_handler(current_page_error, pagination_call.filter(page='current_page'))
    dp.register_callback_query_handler(show_chosen_page, pagination_call.filter(key='flat'), state=FlatStates.flat_data)
