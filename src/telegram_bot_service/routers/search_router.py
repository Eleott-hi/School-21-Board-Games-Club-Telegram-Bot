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
from services.utils import display_fetching_message

router = Router()


@router.callback_query(F.data == "list")
async def show_all_games(query: CallbackQuery):
    message = query.message

    fetching_task = asyncio.create_task(get_all_games())
    display_task = asyncio.create_task(display_fetching_message(message))
    games = await fetching_task
    display_task.cancel()

    buttons, callbacks = form_game_buttons(games)

    answer = dict(
        media=InputMediaPhoto(
            media=FSInputFile("resources/static/menu.jpg"),
            caption=f"There is a list of our games (amount={len(games)})",
        ),
        reply_markup=inline_builder(
            buttons + ["⬅️ Back"],
            callbacks + ["main_menu"],
            sizes=[1],
        ),
    )

    await message.edit_media(**answer)
    await query.answer()


