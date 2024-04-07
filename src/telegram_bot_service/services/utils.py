from typing import List, Dict
import asyncio
from random import choice

EMODJI_ANIMATIONS = [
    ['🌍', '🌎', '🌏'],  # Spinning planet
    ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],  # Moon phases
    ['☀️', '🌤️', '🌥️', '🌦️', '🌧️', '🌩️', '🌧️', '🌦️', '🌥️', '🌤️'],  # Sun and clouds
    ['❄️', '❄️❄️', '❄️❄️❄️', '❄️❄️'],  # Snowflakes
    ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],  # Dots
]


def async_wait(time: int = 2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(time)
            res = await func(*args, **kwargs)
            return res

        return wrapper
    return decorator


async def display_fetching_message(message):
    animation = choice(EMODJI_ANIMATIONS)
    while True:
        for char in animation:
            await message.edit_text(f"Fetching data {char}")
            await asyncio.sleep(0.1)
