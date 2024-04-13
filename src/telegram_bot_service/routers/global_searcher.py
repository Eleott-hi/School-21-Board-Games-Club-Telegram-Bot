from aiogram import Router, F
from services.game_service import get_games_by_str_in_title, get_games_with_filters
from aiogram.types import Message, CallbackQuery
from database.database import MDB
from config import PAGINATION_LIMIT
from routers.common import (
    display_game_list,
    display_game_menu,
    display_game_not_found,
)

router = Router()


@router.message()
async def find_games_according_to_input(message: Message, db: MDB):
    """
    Find games according to input
    """

    title = message.text
    await db.games_paginator_filter.replace_one(
        {"_id": message.from_user.id},
        {"offset": 0, "limit": PAGINATION_LIMIT, "title": title},
        upsert=True,
    )

    replaced_document = await db.games_paginator_filter.find_one(
        {"_id": message.from_user.id}, {"_id": 0}
    )

    data = await get_games_with_filters(replaced_document)

    if not data["total"]:
        await display_game_not_found(message, title, edit=False)

    elif data["total"] == 1:
        await display_game_menu(message, data["games"][0], edit=False)

    else:
        await display_game_list(message, data, 0, edit=False)


@router.callback_query(F.data == "Not implemented")
async def not_implemented_callback(query: CallbackQuery):
    print("Entering not implemented callback", flush=True)
    await query.answer(cache_time=60)
