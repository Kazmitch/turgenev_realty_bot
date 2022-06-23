from aiogram.dispatcher.filters.state import StatesGroup, State


class FlatStates(StatesGroup):
    building_name = State()
    # level = State()
    flat_area = State()
    flat_price = State()
    flat_year = State()
    flat_rooms = State()
    # flat_floor = State()
    flat_data = State()
