from math import ceil
from typing import Dict, Optional
from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from callbacks.callback_data import Screen, Transfer
from keyboards.buttons import pagination_buttons, to_main_menu_button


def main_menu_keyboard():
    kb = [
        [
            InlineKeyboardButton(
                text="Games",
                callback_data=Transfer(to_=Screen.ALL_GAMES_QUERY).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Filters",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Profile",
                callback_data=Transfer(to_=Screen.NOT_IMPLEMENTED).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="Help",
                callback_data=Transfer(to_=Screen.NOT_IMPLEMENTED).pack(),
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def games_list_keyboard(data: dict):
    kb = [
        [
            InlineKeyboardButton(
                text=game["title"],
                callback_data=Transfer(
                    to_=Screen.GAME_MENU,
                    from_=Screen.PAGINATION,
                    meta_=game["id"],
                ).pack(),
            )
        ]
        for game in data["games"]
    ]

    pages = ceil(data["total"] / data["limit"])
    info = f"📄 {data['offset'] + 1}/{pages}"
    pagination = pagination_buttons(data["has_prev"], data["has_next"], info)

    kb = [
        *kb,
        [*pagination],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def game_menu_keyboard(game_id: str, from_: Optional[Screen]):

    back_row = []
    if from_:
        back_row = [
            [
                InlineKeyboardButton(
                    text="⬅️ Back",
                    callback_data=Transfer(to_=from_).pack(),
                )
            ]
        ]
    back_row.append(
        [
            to_main_menu_button,
        ]
    )

    kb = [
        [
            InlineKeyboardButton(
                text="Info",
                callback_data=Transfer(
                    to_=Screen.GAME_INFO,
                    from_=from_,
                    meta_=game_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text="Booking",
                callback_data=Transfer(
                    to_=Screen.CALENDAR,
                    from_=from_,
                    meta_=game_id,
                ).pack(),
            ),
        ],
        *back_row,
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def filter_search_keyboard(filters: Dict):
    kb = [
        [
            InlineKeyboardButton(
                text=f"Number of Players: {filters.get('number_of_players', 'Any')}",
                callback_data=Transfer(to_=Screen.NUMBER_OF_PLAYERS_FILTER).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Duration: {filters.get('duration', 'Any')}",
                callback_data=Transfer(to_=Screen.DURATION_FILTER).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Complexity: {filters.get('complexity', 'Any')}",
                callback_data=Transfer(to_=Screen.COMPLEXITY_FILTER).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Age: {filters.get('age', 'Any')}",
                callback_data=Transfer(to_=Screen.AGE_FILTER).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Genre: {filters.get('genre', 'Any')}",
                callback_data=Transfer(to_=Screen.GENRE_FILTER).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Status: {filters.get('status', 'Any')}",
                callback_data=Transfer(to_=Screen.STATUS_FILTER).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Reset",
                callback_data=Transfer(to_=Screen.RESET_FILTERS).pack(),
            ),
            InlineKeyboardButton(
                text="Search",
                callback_data=Transfer(to_=Screen.FILTERED_GAMES_QUERY).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def number_of_players_kb():
    kb = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=Transfer(
                to_=Screen.NUMBER_OF_PLAYERS_FILTER_RETURN, meta_=str(i)
            ).pack(),
        )
        for i in range(1, 20)
    ]

    kb = [
        kb,
        [
            InlineKeyboardButton(
                text="Any",
                callback_data=Transfer(
                    to_=Screen.NUMBER_OF_PLAYERS_FILTER_RETURN
                ).pack(),
            ),
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def duartion_kb():
    kb = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=Transfer(
                to_=Screen.DURATION_FILTER_RETURN, meta_=str(i)
            ).pack(),
        )
        for i in [15, 30, 45, 60, 180]
    ]

    kb = [
        kb,
        [
            InlineKeyboardButton(
                text="Any",
                callback_data=Transfer(to_=Screen.DURATION_FILTER_RETURN).pack(),
            ),
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def complexity_kb():
    kb = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=Transfer(
                to_=Screen.COMPLEXITY_FILTER_RETURN, meta_=str(i)
            ).pack(),
        )
        for i in ["Easy", "Medium", "Hard"]
    ]

    kb = [
        kb,
        [
            InlineKeyboardButton(
                text="Any",
                callback_data=Transfer(to_=Screen.COMPLEXITY_FILTER_RETURN).pack(),
            ),
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def age_kb():
    kb = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=Transfer(to_=Screen.AGE_FILTER_RETURN, meta_=str(i)).pack(),
        )
        for i in range(1, 19)
    ]

    kb = [
        kb,
        [
            InlineKeyboardButton(
                text="Any",
                callback_data=Transfer(to_=Screen.AGE_FILTER_RETURN).pack(),
            ),
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def genre_kb():
    kb = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=Transfer(to_=Screen.GENRE_FILTER_RETURN, meta_=str(i)).pack(),
        )
        for i in ["Action", "Strategy", "RPG"]
    ]

    kb = [
        kb,
        [
            InlineKeyboardButton(
                text="Any",
                callback_data=Transfer(to_=Screen.GENRE_FILTER_RETURN).pack(),
            ),
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


def status_kb():
    kb = [
        [
            InlineKeyboardButton(
                text=str(i),
                callback_data=Transfer(
                    to_=Screen.STATUS_FILTER_RETURN, meta_=str(i)
                ).pack(),
            )
            for i in ["Available", "Unavailable"]
        ],
        [
            InlineKeyboardButton(
                text="Any",
                callback_data=Transfer(to_=Screen.STATUS_FILTER_RETURN).pack(),
            ),
            InlineKeyboardButton(
                text="⬅️ Back",
                callback_data=Transfer(to_=Screen.GAME_FILTER_MENU).pack(),
            ),
        ],
        [
            to_main_menu_button,
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
