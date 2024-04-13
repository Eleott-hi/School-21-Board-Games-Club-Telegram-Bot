from aiogram.filters.callback_data import CallbackData
from enum import Enum


class PaginationAction(str, Enum):
    PREV = "prev"
    NEXT = "next"


class Pagination(CallbackData, prefix="pagination"):
    # offset: int
    page: int
    # action: PaginationAction


class GameMenu(CallbackData, prefix="game_menu"):
    id: str
    page: int


class GameInfo(CallbackData, prefix="game_info"):
    id: str


class GameBooking(CallbackData, prefix="game_booking"):
    id: str
