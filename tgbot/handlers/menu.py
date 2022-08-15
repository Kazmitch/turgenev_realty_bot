from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from tgbot.keyboards.building_menu import main_building_menu, menu_cd
from tgbot.states.flat_selection import FlatStates
from tgbot.utils.analytics import log_stat
from tgbot.utils.dp_api.db_commands import get_userbot, get_building


async def menu(call: Union[CallbackQuery, Message], state: FSMContext, callback_data: dict = None, **kwargs):
    if isinstance(call, Message):
        message = call
        user = await get_userbot(message.from_user.id)
        building_name = user.building_name
        markup = await main_building_menu(building_name)
        building = await get_building(building_name)
        data = await state.get_data()
        msg_id = int(data.get('msg_id'))
        await state.finish()
        await FlatStates.flat_data.set()
        await message.answer(text=f"Привет, {message.from_user.full_name}!", reply_markup=ReplyKeyboardRemove())
        await message.answer(text=f"Вы находитесь в главном меню {building.name}!", reply_markup=markup)
        await message.bot.delete_message(message.chat.id, msg_id)
        await message.delete()
        await log_stat(message.from_user, event='Отказ отправки контакта')
    elif isinstance(call, CallbackQuery):
        building_name = callback_data.get('name')
        markup = await main_building_menu(building_name)
        await state.finish()
        await FlatStates.flat_data.set()
        await call.message.edit_reply_markup(reply_markup=markup)
        await log_stat(call.from_user, event='Возврат в главное меню')


def register_menu(dp: Dispatcher):
    dp.register_message_handler(menu, text='В начало', state='*')
    dp.register_callback_query_handler(menu, menu_cd.filter(), state='*')
