from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from tgbot.keyboards.about_project import about_project_keyboard, project_cd, photo_gallery_keyboard, photos_keyboard, \
    photo_gallery_cd
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.special_offers import special_offers_keyboard, special_offer_cd, current_offer_menu
from tgbot.states.send_contact import ContactStates
from tgbot.states.special_offers import SpecialOffer
from tgbot.utils.dp_api.db_commands import get_developer_description, get_special_offer_description


async def special_offers(call: CallbackQuery, callback_data: dict,  state: FSMContext, **kwargs):
    """Хендлер на кнопку 'Спецпредложения'."""
    building_name = callback_data.get('name')
    markup = await special_offers_keyboard(building_name)
    await call.message.answer(text='Нашел для вас спецпредложения', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    await SpecialOffer.offer.set()


async def show_current_offer(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Хендлер на показ конкретного предложения."""
    data = await state.get_data()
    building_name = callback_data.get('name')
    offer_id = int(callback_data.get('offer_id'))
    offer_description = await get_special_offer_description(offer_id)
    markup = await current_offer_menu(building_name=building_name)
    await call.message.answer(text=offer_description, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


def register_show_special_offers(dp: Dispatcher):
    dp.register_callback_query_handler(special_offers, building.filter(section='offers'), state='*')
    dp.register_callback_query_handler(show_current_offer, special_offer_cd.filter(), state='*')
