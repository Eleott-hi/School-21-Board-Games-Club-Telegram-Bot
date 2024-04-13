import asyncio

from typing import List, Dict
from random import choice
from aiogram.types import (
    InputMediaPhoto,
    FSInputFile,
    Message,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    KeyboardButton,
)

from keyboards.builders import inline_builder


EMODJI_ANIMATIONS = [
    ["🌍", "🌎", "🌏"],  # Spinning planet
    ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],  # Moon phases
    ["☀️", "🌤️", "🌥️", "🌦️", "🌧️", "🌩️", "🌧️", "🌦️", "🌥️", "🌤️"],  # Sun and clouds
    ["❄️", "❄️❄️", "❄️❄️❄️", "❄️❄️"],  # Snowflakes
    ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],  # Dots
]


def async_wait(time: float = 0.1):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(time)
            res = await func(*args, **kwargs)
            return res

        return wrapper

    return decorator


async def display_fetching_message(message: Message, on_cance_callback: str = None):
    animation = choice(EMODJI_ANIMATIONS)
    is_first_modified = False

    keyboard = inline_builder(
        ["❌ Cancel"],
        [on_cance_callback or "Not implemented"],
    )

    while True:
        for char in animation:
            await asyncio.sleep(0.1)
            if not is_first_modified:

                await message.edit_media(
                    media=InputMediaPhoto(
                        media=FSInputFile("resources/static/loading.jpg"),
                        caption=f"Loading {char}",
                    ),
                    reply_markup=keyboard,
                )

            else:

                await message.edit_media(
                    media=InputMediaPhoto(
                        media=FSInputFile("resources/static/loading.jpg"),
                        caption=f"Loading {char}",
                    ),
                )

            is_first_modified = True
