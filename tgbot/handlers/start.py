import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.keyboards.building_menu import main_building_menu
from tgbot.states.find_building import BuildingState
from tgbot.utils.dp_api.db_commands import get_building, get_find_building
# from realty_bot.realty.models import Developer, Address, Building


async def start_deep_link(message: Message):
    """Переход сразу в меню конкретного ЖК."""
    args = message.get_args()
    await message.answer(f"Привет, {message.from_user.full_name}!")
    building = await get_building(args)
    markup = await main_building_menu(building.latin_name)
    await message.answer(text=f'Меню {building.name}', reply_markup=markup)


async def start(message: Message):
    """Предлагаем пользователю ввести название ЖК."""
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer(f"Введите название ЖК, который вас интересует")
    await BuildingState.name.set()


async def show_find_building(message: Message, state: FSMContext):
    """Выводим меню искомого ЖК."""
    building_name = message.text
    building = await get_find_building(building_name)
    markup = await main_building_menu(building.latin_name)
    await message.answer(text=f'Меню {building.name}', reply_markup=markup)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_deep_link, CommandStart(deep_link=re.compile(r"^[a-z0-9_-]{3,15}$")), state="*")
    dp.register_message_handler(start, CommandStart(), state="*")
    dp.register_message_handler(show_find_building, state=BuildingState.name)
