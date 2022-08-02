from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData


building = CallbackData('building', 'name', 'section')
menu_cd = CallbackData('menu', 'name')


async def main_building_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для выбранного ЖК."""
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='🏡 О проекте',
                                              callback_data=building.new(name=building_name, section='project')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🔑 Подобрать квартиру/планировки',
                                              callback_data=building.new(name=building_name, section='flats')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🎁 Специальные предложения',
                                              callback_data=building.new(name=building_name, section='offers')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🗂 Документация',
                                              callback_data=building.new(name=building_name, section='documents')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='📰 Новости',
                                              callback_data=building.new(name=building_name, section='news')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='📈 Динамика строительства',
                                              callback_data=building.new(name=building_name, section='construction')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='📄 Условия покупки',
                                              callback_data=building.new(name=building_name, section='purchase_terms')
                                          )
                                      ]
                                  ])
    return markup


async def menu_button(building_name: str):
    callback_data = menu_cd.new(name=building_name)
    menu = InlineKeyboardButton(text="↩ В начало", callback_data=callback_data)
    return menu


async def menu_markup(building_name: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(await menu_button(building_name))
    return markup
