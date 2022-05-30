from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


building = CallbackData('building', 'name', 'section')


async def main_building_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для выбранного ЖК."""
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='О проекте',
                                              callback_data=building.new(name=building_name, section='project')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Подобрать квартиру/планировки',
                                              callback_data=building.new(name=building_name, section='flats')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Специальные предложения',
                                              callback_data=building.new(name=building_name, section='offers')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Документация',
                                              callback_data=building.new(name=building_name, section='documents')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Новости',
                                              callback_data=building.new(name=building_name, section='news')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Динамика строительства',
                                              callback_data=building.new(name=building_name, section='constructing')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Условия покупки',
                                              callback_data=building.new(name=building_name, section='purchase_terms')
                                          )
                                      ],
                                  ])
    return markup

menu = InlineKeyboardButton(text="В начало", callback_data="menu")
