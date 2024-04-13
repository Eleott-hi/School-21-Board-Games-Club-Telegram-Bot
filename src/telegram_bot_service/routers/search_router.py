from typing import List, Dict
from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.game_service import get_games_with_filters
from routers.common import display_game_list
from callbacks.callback_data import Pagination
from database.database import MDB
from config import PAGINATION_LIMIT

router = Router()


@router.callback_query(F.data == "list")
async def show_all_games(query: CallbackQuery, db: MDB):
    message = query.message

    await db.games_paginator_filter.replace_one(
        {"_id": query.from_user.id},
        {"offset": 0, "limit": PAGINATION_LIMIT},
        upsert=True,
    )
    replaced_document = await db.games_paginator_filter.find_one(
        {"_id": query.from_user.id}, {"_id": 0}
    )

    response = await get_games_with_filters(replaced_document)

    await display_game_list(message, response, 0, edit=True)

    await query.answer()


@router.callback_query(Pagination.filter())
async def pagination(query: CallbackQuery, callback_data: Pagination, db: MDB):
    message = query.message
    page = callback_data.page

    filter = {"_id": query.from_user.id}
    update = {"$set": {"offset": page}}
    projection = {"_id": 0}
    await db.games_paginator_filter.update_one(filter, update)
    updated_document = await db.games_paginator_filter.find_one(filter, projection)

    data = await get_games_with_filters(updated_document)

    await display_game_list(message, data, page, edit=True)

    await query.answer()
