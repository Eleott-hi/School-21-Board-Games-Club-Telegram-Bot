from services.game_service import get_game_by_id, get_games_with_filters
from routers.common import (
    display_filtered_search,
    display_game_info,
    display_game_list,
    display_game_menu,
    display_main_menu,
)
from typing import Dict
from callbacks.callback_data import Transfer, Screen
from database.database import MDB
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorDatabase as MDB

from config import PAGINATION_LIMIT
from rpc.rpc_client import FibonacciRpcClient
import asyncio

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, db: MDB) -> None:
    await display_main_menu(message, edit=False)


@router.callback_query(Transfer.filter(F.to_ == Screen.MAIN_MENU))
async def main_menu_callback(query: CallbackQuery) -> None:
    message = query.message
    await display_main_menu(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.ALL_GAMES_QUERY))
async def show_all_games(query: CallbackQuery, db: MDB, user_mongo: Dict):
    message = query.message
    user_mongo["filters_for_request"] = {"offset": 0, "limit": PAGINATION_LIMIT}

    data = await get_games_with_filters(user_mongo["filters_for_request"])
    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_game_list(message, data, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.FILTERED_GAMES_QUERY))
async def show_all_games(query: CallbackQuery, db: MDB, user_mongo: Dict):
    message = query.message
    optional_filters = user_mongo.get("optional_filters", {})
    user_mongo["filters_for_request"] = {
        "offset": 0,
        "limit": PAGINATION_LIMIT,
        **optional_filters,
    }

    data = await get_games_with_filters(user_mongo["filters_for_request"])
    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_game_list(message, data, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.PAGINATION))
async def show_all_games(
    query: CallbackQuery,
    db: MDB,
    callback_data: Transfer,
    user_mongo: Dict,
):
    message = query.message

    if callback_data.meta_ == "prev":
        user_mongo["filters_for_request"]["offset"] -= 1
    elif callback_data.meta_ == "next":
        user_mongo["filters_for_request"]["offset"] += 1

    data = await get_games_with_filters(user_mongo["filters_for_request"])
    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_game_list(message, data, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter((F.to_ == Screen.GAME_MENU) & (F.meta_ != None)))
async def game_menu_callback(query: CallbackQuery, callback_data: Transfer, db: MDB):
    message = query.message
    id = callback_data.meta_
    from_ = callback_data.from_

    game = await get_game_by_id(id)
    await display_game_menu(message, game, from_=from_, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter((F.to_ == Screen.GAME_INFO) & (F.meta_ != None)))
async def game_info_callback(query: CallbackQuery, callback_data: Transfer):
    message = query.message
    id = callback_data.meta_
    from_ = callback_data.from_

    game = await get_game_by_id(id)
    await display_game_info(message, game, from_=from_, edit=True)
    await query.answer()


@router.callback_query(
    Transfer.filter((F.to_ == Screen.GAME_BOOKING) & (F.meta_ != None))
)
async def game_booking_callback(query: CallbackQuery, callback_data: Transfer):
    message = query.message
    await query.answer()