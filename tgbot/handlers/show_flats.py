from io import BytesIO

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputFile

from tgbot.keyboards.building_menu import contact_markup
from tgbot.keyboards.flat_pagination import get_page_keyboard, pagination_flats_call
from tgbot.keyboards.flat_selection import flat_selection_cd
from tgbot.states.send_contact import ContactStates
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_xml_link_by_name
from tgbot.utils.images import get_photo_bytes
from tgbot.utils.offers import get_offers, get_photo_url, get_values
from tgbot.utils.page import get_page


async def show_chosen_flats(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    building_name = data.get('building_name') or callback_data.get('building_name')
    ordering = 'area_low_to_high'
    rooms = callback_data.get('option')
    space = callback_data.get('space')
    offers = await get_offers(building_name, rooms, ordering)
    xml_link = await get_xml_link_by_name(building_name)
    plans = None
    if offers:
        max_pages = len(offers)
        offer = await get_page(offers)
        photos = await get_photo_url(offer, xml_link.type_of_xml)
        if len(photos) == 1:
            bytes_photo = BytesIO(await get_photo_bytes(photos[0]))
        elif len(photos) == 2:
            bytes_photo = BytesIO(await get_photo_bytes(photos[0]))
            photo_plan = photos[1]
            if rooms == '5':
                plans = f'<a href="{photo_plan}">Планировка (терраса на кровле)</a>'
            else:
                plans = f'<a href="{photo_plan}">Планировка</a>'
        else:
            bytes_photo = BytesIO(await get_photo_bytes(photos[0]))
            photo_plan1 = photos[1]
            photo_plan2 = photos[2]
            if rooms == '5':
                plans = f'<a href="{photo_plan1}">Планировка (уровень 2/ 8 этаж)</a>\n' \
                        f'<a href="{photo_plan2}">Планировка (терраса на кровле)</a>\n'
            else:
                plans = f'<a href="{photo_plan1}">Планировка</a>\n' \
                        f'<a href="{photo_plan2}">Планировка</a>\n'
        file = InputFile(path_or_bytesio=bytes_photo)
        offer_values = await get_values(offer, xml_link.type_of_xml)
        # price = f'{int(offer_values.get("offer_price").split(".")[0]):_}'.replace('_', ' ')
        await call.message.answer_photo(
            photo=file,
            caption=f'Тип: <b>{offer_values.get("offer_type_of_flat")}</b>\n'
                    f'Площадь: <b>{offer_values.get("offer_area")} м²</b>\n'
                    f'Комнат: <b>{offer_values.get("offer_rooms") if offer_values.get("offer_rooms") else "Не указано"}</b>\n'
                    f'Этаж: <b>{offer_values.get("offer_floor")}</b>\n'
                    f'Секция: <b>{offer_values.get("offer_section")}</b>\n\n'
                    f'{plans if plans else ""}',
            reply_markup=await get_page_keyboard(
                max_pages=max_pages,
                building_name=building_name,
                sort=ordering,
                rooms=rooms,
                space=space
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
    await insert_dict(call.from_user, error='Нажатие на текущую страницу при листании квартир')


async def show_chosen_page(call: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    building_name = data.get('building_name') or callback_data.get('building_name')
    ordering = 'area_low_to_high'
    rooms = callback_data.get('rooms')
    space = callback_data.get('space')
    offers = await get_offers(building_name, rooms, ordering)
    current_page = int(callback_data.get('page'))
    offer = await get_page(offers, page=current_page)
    xml_link = await get_xml_link_by_name(building_name)
    offer_values = await get_values(offer, xml_link.type_of_xml)
    # price = f'{int(offer_values.get("offer_price").split(".")[0]):_}'.replace('_', ' ')
    photos = await get_photo_url(offer, xml_link.type_of_xml)
    plans = None
    if len(photos) == 1:
        bytes_photo = BytesIO(await get_photo_bytes(photos[0]))
    elif len(photos) == 2:
        bytes_photo = BytesIO(await get_photo_bytes(photos[0]))
        photo_plan = photos[1]
        if rooms == '5':
            plans = f'<a href="{photo_plan}">Планировка (терраса на кровле)</a>'
        else:
            plans = f'<a href="{photo_plan}">Планировка</a>'
    else:
        bytes_photo = BytesIO(await get_photo_bytes(photos[0]))
        photo_plan1 = photos[1]
        photo_plan2 = photos[2]
        if rooms == '5':
            plans = f'<a href="{photo_plan1}">Планировка (уровень 2/ 8 этаж)</a>\n' \
                    f'<a href="{photo_plan2}">Планировка (терраса на кровле)</a>\n'
        else:
            plans = f'<a href="{photo_plan1}">Планировка</a>\n' \
                    f'<a href="{photo_plan2}">Планировка</a>\n'
    file = InputFile(path_or_bytesio=bytes_photo)
    media = InputMediaPhoto(media=file,
                            caption=f'Тип: <b>{offer_values.get("offer_type_of_flat")}</b>\n'
                                    f'Площадь: <b>{offer_values.get("offer_area")} м²</b>\n'
                                    f'Комнат: <b>{offer_values.get("offer_rooms") if offer_values.get("offer_rooms") else "Не указано"}</b>\n'
                                    f'Этаж: <b>{offer_values.get("offer_floor")}</b>\n'
                                    f'Секция: <b>{offer_values.get("offer_section")}</b>\n\n'
                                    f'{plans if plans else ""}')
    max_pages = len(offers)
    await call.message.edit_media(
        media=media,
        reply_markup=await get_page_keyboard(
            building_name=building_name,
            max_pages=max_pages,
            page=current_page,
            sort=ordering,
            rooms=rooms,
            space=space
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
    dp.register_callback_query_handler(show_chosen_flats, flat_selection_cd.filter(), state='*')
    dp.register_callback_query_handler(current_page_error, pagination_flats_call.filter(page='current_page'), state='*')
    dp.register_callback_query_handler(show_chosen_page, pagination_flats_call.filter(), state='*')
