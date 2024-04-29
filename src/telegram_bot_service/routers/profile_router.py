from routers.common import (
    display_duration_filter,
    display_filtered_search,
    display_players_num_filter,
    display_age_filter,
    display_complexity_filter,
    display_genre_filter,
    display_status_filter,
)
from typing import Dict
from callbacks.callback_data import Transfer, Screen
from database.database import MDB
from aiogram import F, Router
from aiogram.types import CallbackQuery
from motor.motor_asyncio import AsyncIOMotorDatabase as MDB


router = Router()

@router.callback_query(Transfer.filter(F.to_ == Screen.PROFILE_MENU))
async def start_filters_menu(query: CallbackQuery, user_mongo: Dict) -> None:
    message = query.message
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()

