from aiogram.utils.keyboard import InlineKeyboardButton
from callbacks.callback_data import Transfer, Screen
from typing import Optional

to_main_menu_button = InlineKeyboardButton(
    text="⬅️ Back to Main Menu",
    callback_data=Transfer(to_=Screen.MAIN_MENU).pack(),
)


def pagination_buttons(has_prev: bool, has_next: bool, info: Optional[str] = None):
    kb = []

    if has_prev:
        kb.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=Transfer(to_=Screen.PAGINATION, meta_="prev").pack(),
            )
        )
    else:
        kb.append(
            InlineKeyboardButton(
                text=" ",
                callback_data=Transfer(to_=Screen.IGNORE).pack(),
            )
        )

    kb.append(
        InlineKeyboardButton(
            text=info if info else " ",
            callback_data=Transfer(to_=Screen.IGNORE).pack(),
        )
    )

    if has_next:
        kb.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=Transfer(to_=Screen.PAGINATION, meta_="next").pack(),
            )
        )
    else:
        kb.append(
            InlineKeyboardButton(
                text=" ",
                callback_data=Transfer(to_=Screen.IGNORE).pack(),
            )
        )

    return kb
