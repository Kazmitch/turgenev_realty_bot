import io

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, InputFile

from tgbot.keyboards.about_project import about_project_keyboard, project_cd, photo_gallery_keyboard, photos_keyboard, \
    photo_gallery_cd
from tgbot.keyboards.building_menu import building
from tgbot.keyboards.documentation_keyboard import documents_keyboard, documentation_cd, current_declaration_menu
from tgbot.keyboards.special_offers import special_offers_keyboard, special_offer_cd, current_offer_menu
from tgbot.states.send_contact import ContactStates
from tgbot.states.special_offers import SpecialOffer
from tgbot.utils.dp_api.db_commands import get_developer_description, get_special_offer_description, get_document_file


async def documents(call: CallbackQuery, callback_data: dict,  state: FSMContext, **kwargs):
    """Хендлер на кнопку 'Документация'."""
    building_name = callback_data.get('name')
    markup = await documents_keyboard(building_name)
    await call.message.answer(text='Проектная декларация', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def share_document(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на отправку конкретного документа."""
    await call.answer(cache_time=60)
    building_name = callback_data.get('name')
    document_id = int(callback_data.get('document_id'))
    document = await get_document_file(document_id)
    file = InputFile(path_or_bytesio=document.name)
    markup = await current_declaration_menu(building_name)
    await call.message.answer_document(file, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


def register_documentation(dp: Dispatcher):
    dp.register_callback_query_handler(documents, building.filter(section='documents'), state='*')
    dp.register_callback_query_handler(share_document, documentation_cd.filter(), state='*')
