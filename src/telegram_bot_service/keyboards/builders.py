from typing import List
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def inline_builder(
    text: List[str],
    callback_data: List[str],
    sizes: List[str] = None,
    **kwargs,
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for txt, cb in zip(text, callback_data):
        builder.button(text=txt, callback_data=cb)
    if sizes:
        builder.adjust(*sizes)
    keyboard = builder.as_markup(**kwargs)

    return keyboard
