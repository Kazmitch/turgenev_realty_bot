from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.building_menu import building, menu_markup
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_sales_department, get_userbot, get_call_request


async def special_offers(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    building_name = callback_data.get('building_name')
    user = await get_userbot(call.from_user.id)
    source_id = user.get_source_id
    if len(source_id) == 2:
        call_campaign = await get_call_request(building_name=building_name, site_id=source_id.get('site_id'),
                                               campaign_id=source_id.get('campaign_id'))
    else:
        if source_id.get('site_id'):
            call_campaign = await get_call_request(building_name=building_name, site_id=source_id.get('site_id'))
        else:
            call_campaign = await get_call_request(building_name=building_name,
                                                   campaign_id=source_id.get('campaign_id'))
    phone_number = call_campaign.phone_number
    markup = await menu_markup(building_name)
    await call.message.answer(text=f'Получите персональное предложение в офисе продаж Hill8.\n\n'
                                   f'Позвоните по номеру:\n{phone_number}', reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "Получить персональное предложение"')
    await insert_dict(call.from_user, event='Нажатие кнопки "Получить персональное предложение"')


def register_show_special_offers(dp: Dispatcher):
    dp.register_callback_query_handler(special_offers, building.filter(section='offers'), state='*')
