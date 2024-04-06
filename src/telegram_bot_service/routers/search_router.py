
from typing import List, Dict
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from services.utils import filter_by_title, get_game_by_id, get_all_games
from keyboards.builders import inline_builder
from services.game_service import pritify_game_info, form_game_buttons

router = Router()

@router.callback_query(F.data == "list")
async def show_all_games(query: CallbackQuery):
    games = get_all_games()
    buttons, callbacks = form_game_buttons(games)
    
    await query.message.answer(
        text=f"There is a list of our games (amount={len(games)})",
        reply_markup=inline_builder(
            buttons + ["⬅️ Back"], 
            callbacks + ["main_menu"], 
            sizes=[1],
        ),
    )
    await query.answer()


@router.message()
async def find_games_according_to_input(message: Message):

    games = filter_by_title(message.text)

    if not games:
        await message.answer(f"No games found on request: {message.text}")
    
    elif len(games) == 1:
        await message.answer(
            text=pritify_game_info(games[0]),
            reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
        )
    else:
        buttons, callbacks = form_game_buttons(games)
        await message.answer(
            text=f"Found {len(games)} games on request: {message.text}",
            reply_markup=inline_builder(
                buttons + ["⬅️ Back"], 
                callbacks + ["main_menu"], 
                sizes=[1],
            ),
        )

    
@router.callback_query(F.data.regexp("^game_info_callback:"))
async def game_info_callbacks(query: CallbackQuery):
    print("Game info callback:", query.data)

    id = query.data.replace("game_info_callback:", "").strip()
    game = get_game_by_id(id)

    await query.message.edit_text(
            text=pritify_game_info(game),
            reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
    )
    
    await query.answer()