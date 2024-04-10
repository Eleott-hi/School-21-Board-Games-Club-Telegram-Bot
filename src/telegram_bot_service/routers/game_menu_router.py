import asyncio
from typing import List, Dict
from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ChosenInlineResult,
    InputMediaPhoto,
    FSInputFile,
)
import aiogram.types
from aiogram.fsm.context import FSMContext
from keyboards.builders import inline_builder
from services.game_service import (
    pritify_game_info,
    form_game_buttons,
    get_games_by_str_in_title,
    get_game_by_id,
    get_all_games,
)
from services.utils import (
    display_fetching_message,
)

router = Router()


def extract_id_from_callback_data(dropout_str: str = ""):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            query = args[0]
            id = query.data.replace(dropout_str, "").strip()
            res = await func(*args, id=id, **kwargs)

            return res

        return wrapper

    return decorator


@router.callback_query(F.data.regexp("game_menu_callback:"))
@extract_id_from_callback_data(dropout_str="game_menu_callback:")
async def game_menu_callback(query: CallbackQuery, id: str = None, **kwarg):
    message = query.message

    fetching_task = asyncio.create_task(get_game_by_id(id))
    display_task = asyncio.create_task(display_fetching_message(message))
    game = await fetching_task
    display_task.cancel()

    keyboard = inline_builder(
        ["Info", "Booking", "⬅️ Back"],
        [f"game_info_callback:{id}", f"game_booking_callback:{id}", "main_menu"],
        sizes=[2],
    )

    await message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(game["photo_link"]),
            caption=f"{game['gameName']}, {game['year']}",
        ),
        reply_markup=keyboard,
    )

    await query.answer()


@router.callback_query(F.data.regexp("game_info_callback:"))
@extract_id_from_callback_data(dropout_str="game_info_callback:")
async def game_info_callback(query: CallbackQuery, id: str = None, **kwarg):
    message = query.message

    fetching_task = asyncio.create_task(get_game_by_id(id))
    display_task = asyncio.create_task(display_fetching_message(message))
    game = await fetching_task
    display_task.cancel()

    await message.edit_media(
        media=InputMediaPhoto(
            media=FSInputFile(game["photo_link"]),
            caption=pritify_game_info(game),
        ),
        reply_markup=inline_builder(["⬅️ Back"], [f"game_menu_callback:{id}"]),
    )

    await query.answer()
