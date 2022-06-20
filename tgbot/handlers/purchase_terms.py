from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.building_menu import building
from tgbot.keyboards.purchase_terms import purchase_terms_keyboard, purchase_terms_cd, banks_keyboard, \
    bank_terms_keyboard, term_keyboard, bank_term_cd, installments_keyboard, installment_keyboard, installments_cd, \
    it_mortgage_keyboard, benefit_term_keyboard, benefit_terms_keyboard, benefits_keyboard, benefit_term_cd
from tgbot.utils.dp_api.db_commands import get_current_term, get_installment_term, get_it_mortgage, \
    get_current_benefit_term


async def terms(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Условия покупки'."""
    building_name = callback_data.get('name')
    markup = await purchase_terms_keyboard(building_name)
    await call.message.answer(text='Варианты приобретения', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def banks(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Предложения от банков.'"""
    building_name = callback_data.get('building_name')
    markup = await banks_keyboard(building_name)
    await call.message.answer(text='Выберите банк', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def bank_terms(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на просмотр предложений конкретного банко."""
    building_name = callback_data.get('building_name')
    bank_id = callback_data.get('bank_id')
    markup = await bank_terms_keyboard(building_name, bank_id)
    await call.message.answer(text='Предложения', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_term(call: CallbackQuery, callback_data: dict, **kwargs):
    """Показываем условие банка."""
    building_name = callback_data.get('building_name')
    bank_id = callback_data.get('bank_id')
    term_id = callback_data.get('term_id')
    term = await get_current_term(building_name, bank_id, term_id)
    markup = await term_keyboard(building_name, bank_id)
    await call.message.answer(text=term.description, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def bank_term_navigate(call: CallbackQuery, callback_data: dict, **kwargs):
    # Название ЖК
    building_name = callback_data.get('building_name')

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get('level')

    levels = {
        '0': banks,
        '1': bank_terms,
        '2': show_term
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        building_name=building_name,
        callback_data=callback_data,
    )


async def installments(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Рассрочка'."""
    building_name = callback_data.get('building_name')
    markup = await installments_keyboard(building_name)
    await call.message.answer(text='Виды рассрочек', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_installment(call: CallbackQuery, callback_data: dict, **kwargs):
    """Показываем условие рассрочки."""
    building_name = callback_data.get('building_name')
    installment_id = callback_data.get('installment_id')
    installment = await get_installment_term(building_name, installment_id)
    markup = await installment_keyboard(building_name)
    await call.message.answer(text=installment.description, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def benefits(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на кнопку 'Специальные условия'."""
    building_name = callback_data.get('building_name')
    markup = await benefits_keyboard(building_name)
    await call.message.answer(text='Выберите льготную программу', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def benefit_terms(call: CallbackQuery, callback_data: dict, **kwargs):
    """Хендлер на просмотр условий конкретной льготы."""
    building_name = callback_data.get('building_name')
    benefit_id = callback_data.get('benefit_id')
    markup = await benefit_terms_keyboard(building_name, benefit_id)
    await call.message.answer(text='Условия', reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def show_benefit_term(call: CallbackQuery, callback_data: dict, **kwargs):
    """Показываем условие льготы."""
    building_name = callback_data.get('building_name')
    benefit_id = callback_data.get('benefit_id')
    term_id = callback_data.get('term_id')
    benefit_term = await get_current_benefit_term(building_name, benefit_id, term_id)
    markup = await benefit_term_keyboard(building_name, benefit_id)
    await call.message.answer(text=benefit_term.description, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


async def benefit_term_navigate(call: CallbackQuery, callback_data: dict, **kwargs):
    # Название ЖК
    building_name = callback_data.get('building_name')

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get('level')

    levels = {
        '0': benefits,
        '1': benefit_terms,
        '2': show_benefit_term
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        building_name=building_name,
        callback_data=callback_data,
    )


async def show_it_mortgage(call: CallbackQuery, callback_data: dict, **kwargs):
    """Показываем условие it-ипотеки."""
    building_name = callback_data.get('building_name')
    it_term = await get_it_mortgage(building_name)
    markup = await it_mortgage_keyboard(building_name)
    await call.message.answer(text=it_term.description, reply_markup=markup)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()


def register_purchase_terms(dp: Dispatcher):
    dp.register_callback_query_handler(terms, building.filter(section='purchase_terms'), state='*')
    dp.register_callback_query_handler(banks, purchase_terms_cd.filter(term='banks_mortgage'), state='*')
    dp.register_callback_query_handler(bank_term_navigate, bank_term_cd.filter(), state='*')
    dp.register_callback_query_handler(installments, purchase_terms_cd.filter(term='installment'), state='*')
    dp.register_callback_query_handler(show_installment, installments_cd.filter(), state='*')
    dp.register_callback_query_handler(benefits, purchase_terms_cd.filter(term='conditions'), state='*')
    dp.register_callback_query_handler(benefit_term_navigate, benefit_term_cd.filter(), state='*')
    dp.register_callback_query_handler(show_it_mortgage, purchase_terms_cd.filter(term='it_mortgage'), state='*')
