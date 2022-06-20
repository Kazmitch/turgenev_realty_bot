from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.send_contact import contact_button
from tgbot.utils.dp_api.db_commands import get_banks, get_bank_terms, get_installments, get_benefit_terms, get_benefits

purchase_terms_cd = CallbackData('terms', 'building_name', 'term')
bank_term_cd = CallbackData('bank_term', 'building_name', 'level', 'bank_id', 'term_id')
installments_cd = CallbackData('installment', 'building_name', 'installment_id')
benefit_term_cd = CallbackData('benefit', 'building_name', 'level', 'benefit_id', 'term_id')


def make_bank_callback_data(building_name, level, bank_id='', term_id=''):
    return bank_term_cd.new(building_name=building_name, level=level, bank_id=bank_id, term_id=term_id)


def make_benefit_callback_data(building_name, level, benefit_id='', term_id=''):
    return benefit_term_cd.new(building_name=building_name, level=level, benefit_id=benefit_id, term_id=term_id)


async def purchase_terms_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Условия покупки'."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='Ипотека - предложения от банков',
                callback_data=purchase_terms_cd.new(building_name=building_name, term='banks_mortgage')
            )
        ],
        [
            InlineKeyboardButton(
                text='Рассрочка',
                callback_data=purchase_terms_cd.new(building_name=building_name, term='installment')
            )
        ],
        [
            InlineKeyboardButton(
                text='Ипотека на специальных условиях',
                callback_data=purchase_terms_cd.new(building_name=building_name, term='conditions')
            )
        ],
        [
            InlineKeyboardButton(
                text='Ипотека для IT-специалистов',
                callback_data=purchase_terms_cd.new(building_name=building_name, term='it_mortgage')
            )
        ]
    ]

    markup.row(await menu_button(building_name))

    return markup


async def banks_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Предложения от банков'."""

    # Указываем, что текущий уровень меню - 0
    current_level = 0

    markup = InlineKeyboardMarkup(row_width=1)

    banks = await get_banks(building_name)

    for bank in banks:
        button_text = bank.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=make_bank_callback_data(level=current_level + 1, building_name=building_name,
                                                      bank_id=bank.id)
            )
        )
    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=building.new(name=building_name, section='purchase_terms')
        )
    )

    markup.row(await menu_button(building_name))

    return markup


async def bank_terms_keyboard(building_name: str, bank_id: int) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с предложениями банка."""

    # Указываем, что текущий уровень меню - 1
    current_level = 1

    markup = InlineKeyboardMarkup(row_width=1)

    terms = await get_bank_terms(building_name, bank_id)

    for term in terms:
        button_text = term.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=make_bank_callback_data(level=current_level + 1, building_name=building_name,
                                                      bank_id=str(bank_id), term_id=term.id)
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=make_bank_callback_data(level=current_level - 1, building_name=building_name)
        )
    )

    markup.row(await menu_button(building_name))

    return markup


async def term_keyboard(building_name: str, bank_id: int) -> InlineKeyboardMarkup:
    """Выводим условие банка."""

    # Указываем, что текущий уровень меню - 2
    current_level = 2

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=make_bank_callback_data(level=current_level - 1, building_name=building_name,
                                                  bank_id=str(bank_id))
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def installments_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру с вариантами рассрочек."""

    markup = InlineKeyboardMarkup(row_width=1)

    installments = await get_installments(building_name)

    for installment in installments:
        button_text = installment.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=installments_cd.new(building_name=building_name, installment_id=installment.id)
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=building.new(name=building_name, section='purchase_terms')
        )
    )

    markup.row(await menu_button(building_name))

    return markup


async def installment_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Выводим условие рассрочки."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=purchase_terms_cd.new(building_name=building_name, term='installment')
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def benefits_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Ипотека на специальных условиях'."""

    # Указываем, что текущий уровень меню - 0
    current_level = 0

    markup = InlineKeyboardMarkup(row_width=1)

    benefits = await get_benefits(building_name)

    for benefit in benefits:
        button_text = benefit.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=make_benefit_callback_data(level=current_level + 1, building_name=building_name,
                                                         benefit_id=benefit.id)
            )
        )
    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=building.new(name=building_name, section='purchase_terms')
        )
    )

    markup.row(await menu_button(building_name))

    return markup


async def benefit_terms_keyboard(building_name: str, benefit_id: int) -> InlineKeyboardMarkup:
    """Создаем клавиатуру са льготами."""

    # Указываем, что текущий уровень меню - 1
    current_level = 1

    markup = InlineKeyboardMarkup(row_width=1)

    benefit_terms = await get_benefit_terms(building_name, benefit_id)

    for benefit_term in benefit_terms:
        button_text = benefit_term.title

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=make_benefit_callback_data(level=current_level + 1, building_name=building_name,
                                                         benefit_id=str(benefit_id), term_id=benefit_term.id)
            )
        )

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=make_benefit_callback_data(level=current_level - 1, building_name=building_name)
        )
    )

    markup.row(await menu_button(building_name))

    return markup


async def benefit_term_keyboard(building_name: str, benefit_id: int) -> InlineKeyboardMarkup:
    """Выводим условие льготы."""

    # Указываем, что текущий уровень меню - 2
    current_level = 2

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=make_benefit_callback_data(level=current_level - 1, building_name=building_name,
                                                     benefit_id=str(benefit_id))
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup


async def it_mortgage_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Выводим условие it-ипотеки."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='Вернуться',
            callback_data=building.new(name=building_name, section='purchase_terms')
        )
    )
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
