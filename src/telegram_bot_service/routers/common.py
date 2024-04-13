import asyncio
from keyboards.builders import inline_builder
from aiogram.types import (
    InputMediaPhoto,
    FSInputFile,
)
from typing import Dict
from services.utils import create_or_edit_media, display_animation
from services.game_service import form_game_buttons, pritify_game_info
from callbacks.callback_data import GameMenu, GameInfo, GameBooking, Pagination
from config import PAGINATION_LIMIT

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
        edit=edit,
    )


async def display_game_menu(message, game, edit):
    keyboard = inline_builder(
        ["Info", "Booking", "⬅️ Back to menu"],
        [
            GameInfo(id=game["id"]).pack(),
            GameBooking(id=game["id"]).pack(),
            "main_menu",
        ],
        sizes=[2],
    )

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
        reply_markup=inline_builder(["⬅️ Back"], [GameMenu(id=game["id"]).pack()]),
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


async def display_game_list(message, data, page, edit):
    
    prev_button, prev_callback = (
        ("⬅️", Pagination(page=page - 1))
        if data["has_prev"]
        else ("❌", "Not implemented")
    )

    next_button, next_callback = (
        ("➡️", Pagination(page=page + 1))
        if data["has_next"]
        else ("❌", "Not implemented")
    )

    pages_count = data["total"] // PAGINATION_LIMIT + (
        1 if data["total"] % PAGINATION_LIMIT else 0
    )
    page_button, page_callback = (f"📄 {page+1}/{pages_count}", "Not implemented")

    buttons, callbacks = form_game_buttons(data["games"])

    keyboard = inline_builder(
        buttons + [prev_button, page_button, next_button] + ["⬅️ Back to menu"],
        callbacks + [prev_callback, page_callback, next_callback] + ["main_menu"],
        sizes=[1] * len(buttons) + [3, 1],
    )

    await create_or_edit_media(
        message,
        photo="resources/static/menu.jpg",
        caption=f"Found {data['total']} games",
        reply_markup=keyboard,
        edit=edit,
    )
