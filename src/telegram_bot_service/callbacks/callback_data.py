from aiogram.filters.callback_data import CallbackData
from enum import Enum
from typing import Optional


class Screen(int, Enum):
    MAIN_MENU = 0
    SEARCH = 1
    ALL_GAMES_QUERY = 3
    PAGINATION = 4
    GAME_FILTER = 5
    GAME_MENU = 6
    GAME_INFO = 7
    GAME_BOOKING = 8
    HELP = 9
    FILTERED_GAMES_QUERY = 10

    # Optional filters callbacks 10X
    GAME_FILTER_MENU = 100
    NUMBER_OF_PLAYERS_FILTER = 101
    DURATION_FILTER = 102
    COMPLEXITY_FILTER = 103
    AGE_FILTER = 104
    GENRE_FILTER = 105
    STATUS_FILTER = 106
    RESET_FILTERS = 107

    # Optional filters callbacks return values 11X
    NUMBER_OF_PLAYERS_FILTER_RETURN = 111
    DURATION_FILTER_RETURN = 112
    COMPLEXITY_FILTER_RETURN = 113
    AGE_FILTER_RETURN = 114
    GENRE_FILTER_RETURN = 115
    STATUS_FILTER_RETURN = 116

    # Booking 20X
    CALENDAR = 201

    # Ignored
    IGNORE = -1
    NOT_IMPLEMENTED = -2
    TMP = -100


class Transfer(CallbackData, prefix="tr"):
    to_: Screen
    meta_: Optional[str] = None
    from_: Optional[Screen] = None
