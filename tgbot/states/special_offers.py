from aiogram.dispatcher.filters.state import StatesGroup, State


class SpecialOffer(StatesGroup):
    offer = State()
