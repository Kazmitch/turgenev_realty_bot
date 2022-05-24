from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def main_building_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для выбранного ЖК."""
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(
                                              text='О проекте',
                                              callback_data=f'{building_name}_project'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Подобрать квартиру/планировки',
                                              callback_data=f'{building_name}_flats'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Специальные предложения',
                                              callback_data=f'{building_name}_offers'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Документация',
                                              callback_data=f'{building_name}_documents'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Новости',
                                              callback_data=f'{building_name}_news'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Динамика строительства',
                                              callback_data=f'{building_name}_constructing'
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='Условия покупки',
                                              callback_data=f'{building_name}_purchase terms'
                                          )
                                      ],
                                  ])
    return markup
