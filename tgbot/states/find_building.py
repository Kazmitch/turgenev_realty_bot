from aiogram.dispatcher.filters.state import StatesGroup, State


class BuildingState(StatesGroup):
    name = State()
