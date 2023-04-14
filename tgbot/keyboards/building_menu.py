from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.flat_selection import flat_selection_cd
from tgbot.keyboards.make_call import call_button
from tgbot.keyboards.send_contact import contact_button

building = CallbackData('building', 'name', 'section')
menu_cd = CallbackData('menu', 'name')


async def main_building_menu(building_name: str) -> InlineKeyboardMarkup:
    """Создаем клавиатуру для выбранного ЖК."""

    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      # [
                                      #     InlineKeyboardButton(
                                      #         text='🏢 Квартиры для жизни и инвестиций',
                                      #         callback_data=building.new(name=building_name, section='business_life')
                                      #     )
                                      # ],
                                      [
                                          InlineKeyboardButton(
                                              text='🟫 О проекте',
                                              callback_data=building.new(name=building_name, section='project')
                                          ),

                                          InlineKeyboardButton(
                                              text='🟫 Подобрать квартиру',
                                              callback_data=building.new(name=building_name, section='flats')
                                          )
                                      ],
                                      [
                                          InlineKeyboardButton(
                                              text='🟫 Подобрать пентхаус',
                                              callback_data=flat_selection_cd.new(building_name=building_name,
                                                                                  option='5', space=0)
                                          ),
                                          await call_button(building_name)
                                      ],
                                      [
                                          await contact_button(building_name)
                                      ]

                                      # [
                                      #     InlineKeyboardButton(
                                      #         text='📄 Условия покупки',
                                      #         callback_data=building.new(name=building_name, section='purchase_terms')
                                      #     )
                                      # ]
                                  ])

    return markup


async def menu_button(building_name: str):
    callback_data = menu_cd.new(name=building_name)
    menu = InlineKeyboardButton(text="🟫 В начало", callback_data=callback_data)
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
