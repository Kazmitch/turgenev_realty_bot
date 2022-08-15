from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.purchase_terms import purchase_terms_keyboard, term_keyboard, purchase_terms_cd
from tgbot.utils.analytics import log_stat
from tgbot.utils.terms import make_term_text


async def terms(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Условия покупки'."""
    building_name = callback_data.get('name')
    markup = await purchase_terms_keyboard(building_name)
    await call.message.answer(text='Варианты приобретения', reply_markup=markup)
    await call.message.delete()
    await log_stat(call.from_user, event='Нажатие кнопки "Условия покупки"')


async def show_term(call: CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    """Выводим условие покупки."""
    building_name = callback_data.get('building_name')
    term = callback_data.get('term')
    text = await make_term_text(building_name, term)
    markup = await term_keyboard(building_name)
    await call.message.answer(text=text, reply_markup=markup)
    await call.message.delete()
    await state.update_data(section=callback_data.get('section'), term=callback_data.get('term'))
    await log_stat(call.from_user, event='Вывод условий покупки')


def register_purchase_terms(dp: Dispatcher):
    dp.register_callback_query_handler(terms, building.filter(section='purchase_terms'), state='*')
    dp.register_callback_query_handler(show_term, purchase_terms_cd.filter(), state='*')
