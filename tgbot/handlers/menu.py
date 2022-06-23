from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.building_menu import main_building_menu, menu_cd
from tgbot.states.flat_selection import FlatStates


async def menu(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    building_name = callback_data.get('name')
    markup = await main_building_menu(building_name)
    await state.finish()
    await FlatStates.flat_data.set()
    await call.message.edit_reply_markup(reply_markup=markup)


def register_menu(dp: Dispatcher):
    dp.register_callback_query_handler(menu, menu_cd.filter(), state='*')
