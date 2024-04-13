from aiogram import Router
from services.game_service import get_games_by_str_in_title
from aiogram.types import Message
from routers.common import (
    display_game_list,
    display_game_menu,
    display_game_not_found,
)

router = Router()


@router.message()
async def find_games_according_to_input(message: Message):
    """
    Find games according to input
    """

    title = message.text
    games = await get_games_by_str_in_title(title)

    if not games:
        await display_game_not_found(message, title, edit=False)
    elif len(games) == 1:
        await display_game_menu(message, games[0], edit=False)
    else:
        await display_game_list(message, games, edit=False)
