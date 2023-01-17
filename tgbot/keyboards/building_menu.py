from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button, contact_cd

building = CallbackData('building', 'name', 'section')
menu_cd = CallbackData('menu', 'name')


async def main_building_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для выбранного ЖК."""
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='🏢 Апартаменты для бизнеса и жизни',
                                              callback_data=building.new(name=building_name, section='business_life')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🔑 Подобрать апартаменты',
                                              callback_data=building.new(name=building_name, section='flats')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🏡 О проекте',
                                              callback_data=building.new(name=building_name, section='project')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='📄 Условия оплаты',
                                              callback_data=building.new(name=building_name, section='purchase_terms')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🎁 Получить скидку 25%',
                                              callback_data=building.new(name=building_name, section='offers')
                                          )
                                      ]
                                  ])
    # markup.row(await call_button(building_name))
    # markup.row(await contact_button(building_name))
    return markup


async def special_offer_button(building_name: str):
    callback_data = building.new(name=building_name, section='offers')
    offer = InlineKeyboardButton(text='🎁 Получить скидку 25%', callback_data=callback_data)
    return offer


async def menu_button(building_name: str):
    callback_data = menu_cd.new(name=building_name)
    menu = InlineKeyboardButton(text="↩ В начало", callback_data=callback_data)
    return menu


async def menu_markup(building_name: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(await menu_button(building_name))
    return markup


async def contact_markup(building_name: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(await contact_button(building_name))
    markup.row(await menu_button(building_name))
    return markup
