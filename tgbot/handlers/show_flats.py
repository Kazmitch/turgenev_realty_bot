from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.states.flat_selection import FlatStates
from tgbot.utils.dp_api.db_commands import get_xml_link_by_name
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
    offers = await get_offers_yan(xml_link, area, price)
    await call.message.answer("The best")


def register_show_flats(dp: Dispatcher):
    dp.register_callback_query_handler(show_flats, text='show_flats', state=FlatStates.flat_data)
