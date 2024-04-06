from typing import List
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, InlineKeyboardBuilder, InlineKeyboardMarkup


def inline_builder(
    text: List[str],
    callback_data: List[str],
    sizes: List[str] = None,
    **kwargs,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for txt, cb in zip(text, callback_data):
        builder.button(text=txt, callback_data=cb)
    if sizes:
        builder.adjust(*sizes)
        
    keyboard = builder.as_markup(**kwargs)

    return keyboard

def reply_builder(
    text: List[str],
    callback_data: List[str],
    sizes: List[str] = None,
    **kwargs,
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for txt, cb in zip(text, callback_data):
        builder.button(text=txt, callback_data=cb)
    if sizes:
        builder.adjust(*sizes)

    keyboard = builder.as_markup(**kwargs)

    return keyboard

