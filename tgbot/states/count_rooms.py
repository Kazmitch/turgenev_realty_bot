from aiogram.dispatcher.filters.state import StatesGroup, State


class CountRoomsStates(StatesGroup):
    count = State()
