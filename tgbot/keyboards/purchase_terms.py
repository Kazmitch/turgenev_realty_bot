from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.building_menu import menu_button, building
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

purchase_terms_cd = CallbackData('terms', 'building_name', 'section', 'term')


async def purchase_terms_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру на кнопку 'Условия покупки'."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.inline_keyboard = [
        [
            InlineKeyboardButton(
                text='🏦 Ипотека - предложения от банков',
                callback_data=purchase_terms_cd.new(building_name=building_name, section='purchase_terms', term='bank')
            )
        ],
        [
            InlineKeyboardButton(
                text='📉 Рассрочка',
                callback_data=purchase_terms_cd.new(building_name=building_name, section='purchase_terms', term='installment')
            )
        ],
        [
            InlineKeyboardButton(
                text='👨‍👩‍👧‍👦 Ипотека на специальных условиях',
                callback_data=purchase_terms_cd.new(building_name=building_name, section='purchase_terms', term='conditions')
            )
        ],
        [
            InlineKeyboardButton(
                text='👨‍💻 Ипотека для IT-специалистов',
                callback_data=purchase_terms_cd.new(building_name=building_name, section='purchase_terms', term='it_mortgage')
            )
        ]
    ]

    markup.row(await menu_button(building_name))

    return markup


async def term_keyboard(building_name: str) -> InlineKeyboardMarkup:
    """Выводим условие."""

    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text='🔙 Вернуться',
            callback_data=building.new(name=building_name, section='purchase_terms')
        )
    )

    markup.row(await call_button(building_name))
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))

    return markup
