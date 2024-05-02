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
from database.database import database

EMODJI_ANIMATIONS = [
    ["🌍", "🌎", "🌏"],  # Spinning planet
    ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],  # Moon phases
    ["☀️", "🌤️", "🌥️", "🌦️", "🌧️", "🌩️", "🌧️", "🌦️", "🌥️", "🌤️"],  # Sun and clouds
    ["❄️", "❄️❄️", "❄️❄️❄️", "❄️❄️"],  # Snowflakes
    # ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],  # Dots
]


def async_wait(time: float = 0):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(time)
            res = await func(*args, **kwargs)
            return res

        return wrapper

    return decorator


async def display_animation(
    message: Message, task, create_image: bool = False, on_cance_callback: str = None
):
    animation = choice(EMODJI_ANIMATIONS)

    keyboard = inline_builder(
        ["❌ Cancel"],
        [on_cance_callback or Transfer(to=Screen.IGNORE).pack()],
    )

    while True:
        for char in animation:
            # await asyncio.sleep(0.1)

            if create_image:
                message = await message.answer_photo(
                    photo=FSInputFile("resources/static/loading.jpg"),
                    caption=f"Loading {char}",
                    reply_markup=keyboard,
                )
                create_image = False

            else:
                await message.edit_media(
                    media=InputMediaPhoto(
                        media=FSInputFile("resources/static/loading.jpg"),
                        caption=f"Loading {char}",
                    ),
                    reply_markup=keyboard,
                )

            if task.done():
                return message


async def create_or_edit_media(
    message,
    photo: str,
    caption: str,
    reply_markup,
    edit: bool,
):
    if edit:
        await message.edit_media(
            media=InputMediaPhoto(
                media=FSInputFile(photo),
                caption=caption,
            ),
            reply_markup=reply_markup,
        )

    else:
        await message.answer_photo(
            photo=FSInputFile(photo),
            caption=caption,
            reply_markup=reply_markup,
        )


