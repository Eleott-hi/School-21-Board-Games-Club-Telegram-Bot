
import asyncio
from typing import List, Dict
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ChosenInlineResult
import aiogram.types 
from aiogram.fsm.context import FSMContext
from keyboards.builders import inline_builder
from services.game_service import pritify_game_info, form_game_buttons, get_games_by_str_in_title, get_game_by_id, get_all_games

router = Router()

@router.callback_query(F.data == "list")
async def show_all_games(query: CallbackQuery):
    games = await get_all_games()
    buttons, callbacks = form_game_buttons(games)
    
    await query.message.edit_text(
        text=f"There is a list of our games (amount={len(games)})",
        reply_markup=inline_builder(
            buttons + ["⬅️ Back"], 
            callbacks + ["main_menu"], 
            sizes=[1],
        ),
    )
    await query.answer()


@router.message()
async def find_games_according_to_input(message: Message, state: FSMContext):
    title:str = message.text
    await state.set_data({"title": title})
    print(state)
    
    message = await message.answer(f"Searching for games on request: {message.text}")
    
    games = await get_games_by_str_in_title(title)
    # await message_waiting.delete()    

    if not games:
        await message.edit_text(f"No games found on request: {title}")
    
    elif len(games) == 1:
        await message.edit_text(
            text=pritify_game_info(games[0]),
            reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
        )
    else:
        buttons, callbacks = form_game_buttons(games)
        await message.edit_text(
            text=f"Found {len(games)} games on request: {title}",
            reply_markup=inline_builder(
                buttons + ["⬅️ Back"], 
                callbacks + ["main_menu"], 
                sizes=[1],
            ),
        )

    
@router.callback_query(F.data.regexp("game_info_callback:"))
async def game_info_callback(query: CallbackQuery, state: FSMContext):
    
    
    data = await state.get_data()
    title = data.get("title")
    
    print("Game info callback:", query.data, title)

    id = query.data.replace("game_info_callback:", "").strip()
    game = await get_game_by_id(id)

    await query.message.edit_text(
            text=pritify_game_info(game),
            reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
    )
    
    await query.answer()