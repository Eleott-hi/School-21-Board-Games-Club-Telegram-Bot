from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


class MainMenuSG(StatesGroup):
    main = State()


class PaginationSG(StatesGroup):
    main = State()


class GameDialogSG(StatesGroup):
    main = State()
    info = State()
    booking = State()
    collections = State()


class FilterSG(StatesGroup):
    main = State()
    players_num = State()
    duration = State()
    complexity = State()
    age = State()
    genre = State()
    status = State()


class TitleSearchSG(StatesGroup):
    main = State()
    location = State()


class ProfileSG(StatesGroup):
    main = State()
    bookings = State()
    collections = State()
    registration = State()


class OptionsSG(StatesGroup):
    main = State()
    pagination = State()
    language = State()


class TelegramErrorSG(StatesGroup):
    main = State()


class RegistrationSG(StatesGroup):
    start = State()
    confirm = State()


async def not_implemented_yet(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer("Not implemented yet")


async def ignore(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(cache_time=60)
