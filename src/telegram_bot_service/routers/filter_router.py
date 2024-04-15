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


@router.callback_query(Transfer.filter(F.to_ == Screen.GAME_FILTER_MENU))
async def start_filters_menu(query: CallbackQuery, user_mongo: Dict) -> None:
    message = query.message
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.RESET_FILTERS))
async def reset_filters(query: CallbackQuery, db: MDB, user_mongo: Dict):
    message = query.message

    if user_mongo["optional_filters"] != {}:
        user_mongo["optional_filters"] = {}
        await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
        await display_filtered_search(
            message, user_mongo["optional_filters"], edit=True
        )
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.NUMBER_OF_PLAYERS_FILTER))
async def players_num_filter_menu(query: CallbackQuery):
    message = query.message
    await display_players_num_filter(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.NUMBER_OF_PLAYERS_FILTER_RETURN))
async def set_players_num_filter(
    query: CallbackQuery, callback_data: Transfer, db: MDB, user_mongo: Dict
):
    message = query.message
    players_num = callback_data.meta_

    if players_num:
        user_mongo["optional_filters"]["number_of_players"] = int(players_num)
    elif "number_of_players" in user_mongo["optional_filters"]:
        del user_mongo["optional_filters"]["number_of_players"]

    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.DURATION_FILTER))
async def players_num_filter_menu(query: CallbackQuery):
    message = query.message
    await display_duration_filter(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.DURATION_FILTER_RETURN))
async def set_players_num_filter(
    query: CallbackQuery, callback_data: Transfer, db: MDB, user_mongo: Dict
):
    message = query.message
    new_value = callback_data.meta_

    if new_value:
        user_mongo["optional_filters"]["duration"] = int(new_value)
    elif "duration" in user_mongo["optional_filters"]:
        del user_mongo["optional_filters"]["duration"]

    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.COMPLEXITY_FILTER))
async def players_num_filter_menu(query: CallbackQuery):
    message = query.message
    await display_complexity_filter(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.COMPLEXITY_FILTER_RETURN))
async def set_players_num_filter(
    query: CallbackQuery, callback_data: Transfer, db: MDB, user_mongo: Dict
):
    message = query.message
    new_value = callback_data.meta_

    if new_value:
        user_mongo["optional_filters"]["complexity"] = new_value
    elif "complexity" in user_mongo["optional_filters"]:
        del user_mongo["optional_filters"]["complexity"]

    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.AGE_FILTER))
async def players_num_filter_menu(query: CallbackQuery):
    message = query.message
    await display_age_filter(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.AGE_FILTER_RETURN))
async def set_players_num_filter(
    query: CallbackQuery, callback_data: Transfer, db: MDB, user_mongo: Dict
):
    message = query.message
    new_value = callback_data.meta_

    if new_value:
        user_mongo["optional_filters"]["age"] = int(new_value)
    elif "age" in user_mongo["optional_filters"]:
        del user_mongo["optional_filters"]["age"]

    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.GENRE_FILTER))
async def players_num_filter_menu(query: CallbackQuery):
    message = query.message
    await display_genre_filter(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.GENRE_FILTER_RETURN))
async def set_players_num_filter(
    query: CallbackQuery, callback_data: Transfer, db: MDB, user_mongo: Dict
):
    message = query.message
    new_value = callback_data.meta_

    if new_value:
        user_mongo["optional_filters"]["genre"] = new_value
    elif "genre" in user_mongo["optional_filters"]:
        del user_mongo["optional_filters"]["genre"]

    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.STATUS_FILTER))
async def players_num_filter_menu(query: CallbackQuery):
    message = query.message
    await display_status_filter(message, edit=True)
    await query.answer()


@router.callback_query(Transfer.filter(F.to_ == Screen.STATUS_FILTER_RETURN))
async def set_players_num_filter(
    query: CallbackQuery, callback_data: Transfer, db: MDB, user_mongo: Dict
):
    message = query.message
    new_value = callback_data.meta_

    if new_value:
        user_mongo["optional_filters"]["status"] = new_value
    elif "status" in user_mongo["optional_filters"]:
        del user_mongo["optional_filters"]["status"]

    await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)
    await display_filtered_search(message, user_mongo["optional_filters"], edit=True)
    await query.answer()
