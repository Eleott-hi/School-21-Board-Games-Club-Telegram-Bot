import asyncio
from keyboards.builders import inline_builder
from aiogram.types import (
    InputMediaPhoto,
    FSInputFile,
)
from typing import Dict
from services.utils import create_or_edit_media, display_animation
from services.game_service import form_game_buttons, pritify_game_info


# async def with_loading_animation(message, loading_coroutine, create_image=False):
#     loading_task = asyncio.create_task(loading_coroutine)
#     # message = await display_animation(message, loading_task, create_image=create_image)
#     return message, await loading_task


async def display_main_menu(message, edit):
    keyboard = inline_builder(
        ["All games", "Find with options"],
        ["list", "find_with_options"],
        one_time_keyboard=True,
    )

    await create_or_edit_media(
        message=message,
        photo="resources/static/menu.jpg",
        caption="Menu",
        reply_markup=keyboard,
        edit=edit
    )


async def display_game_menu(message, game, edit, back_action: Dict = None):
    """
    Create game menu.
    Message should be MEDIA type message
    """

    buttons = ["Info", "Booking"]
    callbacks = [
        f"game_info_callback:{game['id']}",
        f"game_booking_callback:{game['id']}",
    ]

    if back_action:
        buttons += back_action["buttons"]
        callbacks += back_action["callbacks"]

    keyboard = inline_builder(buttons, callbacks, sizes=[2])

    await create_or_edit_media(
        message=message,
        photo=game["photo_link"],
        caption=f"{game['gameName']}, {game['year']}",
        reply_markup=keyboard,
        edit=edit,
    )


async def display_game_info(message, game, edit):
    await create_or_edit_media(
        message,
        photo=game["photo_link"],
        caption=pritify_game_info(game),
        reply_markup=inline_builder(["⬅️ Back"], [f"game_menu_callback:{game['id']}"]),
        edit=edit,
    )


async def display_game_not_found(message, title, edit):
    await create_or_edit_media(
        message,
        photo="resources/static/not_found.jpg",
        caption=f"No games found on request: {title}",
        reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
        edit=edit,
    )


async def display_game_list(message, games, edit):
    buttons, callbacks = form_game_buttons(games)
    keyboard = inline_builder(
        buttons + ["⬅️ Back"],
        callbacks + ["main_menu"],
        sizes=[1],
    )

    await create_or_edit_media(
        message,
        photo="resources/static/menu.jpg",
        caption=f"Found {len(games)} games",
        reply_markup=keyboard,
        edit=edit,
    )
