from typing import List, Dict
from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.game_service import get_all_games
from routers.common import display_game_list

router = Router()


@router.callback_query(F.data == "list")
async def show_all_games(query: CallbackQuery):
    message = query.message
    games = await get_all_games()
    await display_game_list(message, games,edit=True)
    await query.answer()
