from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.documentation import documents_keyboard, documentation_cd, current_declaration_menu
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_document_file


async def documents(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Хендлер на кнопку 'Документация'."""
    building_name = callback_data.get('name')
    markup = await documents_keyboard(building_name)
    await call.message.answer(text='Проектная декларация', reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "Документация"')
    await insert_dict(call.from_user, event='Нажатие кнопки "Документация"')


async def share_document(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Хендлер на отправку конкретного документа."""
    await call.answer(cache_time=60)
    building_name = callback_data.get('name')
    document_id = int(callback_data.get('document_id'))
    document = await get_document_file(document_id)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{document.name}')
    markup = await current_declaration_menu(building_name)
    await call.message.answer_document(file, reply_markup=markup)
    await call.message.delete()
    await state.update_data(section=callback_data.get('section'))
    await log_stat(call.from_user, event='Просмотр документа')
    await insert_dict(call.from_user, event='Просмотр документа')


def register_documentation(dp: Dispatcher):
    dp.register_callback_query_handler(documents, building.filter(section='documents'), state='*')
    dp.register_callback_query_handler(share_document, documentation_cd.filter(), state='*')
