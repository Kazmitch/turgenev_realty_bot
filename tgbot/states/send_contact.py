from aiogram.dispatcher.filters.state import StatesGroup, State


class ContactStates(StatesGroup):
    building_name = State()
    contact = State()
