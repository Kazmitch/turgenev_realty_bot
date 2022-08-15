from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.building_menu import menu_markup
from tgbot.keyboards.make_call import call_cd
from tgbot.utils.analytics import log_stat
from tgbot.utils.dp_api.db_commands import get_sales_department


async def make_call(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    building_name = callback_data.get('building_name')
    sales_department = await get_sales_department(building_name)
    department_text = sales_department.description
    markup = await menu_markup(building_name)
    await call.message.answer(text=f'{department_text}', reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "Связаться с отделом продаж"')


def register_make_call(dp: Dispatcher):
    dp.register_callback_query_handler(make_call, call_cd.filter(), state='*')
