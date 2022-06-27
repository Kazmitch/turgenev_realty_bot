from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InputFile

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.special_offers import special_offers_keyboard, special_offer_cd, current_offer_menu
from tgbot.utils.dp_api.db_commands import get_special_offer_description


async def special_offers(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Хендлер на кнопку 'Спецпредложения'."""
    building_name = callback_data.get('name')
    markup = await special_offers_keyboard(building_name)
    await call.message.answer(text='😄 На недвижимость в этом ЖК есть скидки! Посмотрим? 🤔', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_current_offer(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Хендлер на показ конкретного предложения."""
    building_name = callback_data.get('name')
    offer_id = int(callback_data.get('offer_id'))
    offer = await get_special_offer_description(offer_id)
    markup = await current_offer_menu(building_name=building_name)
    description = offer.description
    photo = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{offer.photo.name}')
    await call.message.answer_photo(photo=photo, caption=description, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


def register_show_special_offers(dp: Dispatcher):
    dp.register_callback_query_handler(special_offers, building.filter(section='offers'), state='*')
    dp.register_callback_query_handler(show_current_offer, special_offer_cd.filter(), state='*')
