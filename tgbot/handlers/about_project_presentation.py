from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from realty_bot.realty_bot.settings import MEDIA_ROOT
from tgbot.keyboards.about_project import presentation_cd
from tgbot.keyboards.about_project_presentation import current_presentation_keyboard
from tgbot.utils.analytics import log_stat
from tgbot.utils.clickhouse import insert_dict
from tgbot.utils.dp_api.db_commands import get_presentation_file


async def show_presentation(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Хендлер на просмотр презентации."""
    await call.answer(cache_time=60)
    building_name = callback_data.get('building_name')
    presentation_id = int(callback_data.get('pres_id'))
    presentation = await get_presentation_file(presentation_id)
    file = InputFile(path_or_bytesio=f'{MEDIA_ROOT}{presentation.document.name}')
    markup = await current_presentation_keyboard(building_name)
    await call.message.answer_document(file, reply_markup=markup)
    await call.message.delete()
    await state.update_data(section='presentation')
    await log_stat(call.from_user, event='Просмотр презентации')
    await insert_dict(call.from_user, event='Просмотр презентации')


def register_presentation(dp: Dispatcher):
    dp.register_callback_query_handler(show_presentation, presentation_cd.filter(), state='*')
