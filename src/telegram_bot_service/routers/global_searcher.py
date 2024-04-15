from aiogram import Router, F
from services.game_service import get_games_with_filters
from aiogram.types import Message, CallbackQuery
from database.database import MDB
from config import PAGINATION_LIMIT
from routers.common import (
    display_game_list,
    display_game_menu,
    display_game_not_found,
)
from callbacks.callback_data import Screen, Transfer

router = Router()


@router.message()
async def find_games_according_to_input(message: Message, db: MDB):
    title = message.text
    id = message.from_user.id

    user = await db.users.find_one({"_id": id})
    user["filters_for_request"] = {
        "offset": 0,
        "limit": PAGINATION_LIMIT,
        "title": title,
    }
    await db.users.replace_one({"_id": id}, user)

    data = await get_games_with_filters(user["filters_for_request"])

    if data["total"] <= 0:
        caption = f"No game was found on request: {title}"
        await display_game_not_found(message, caption=caption, edit=False)

    elif data["total"] == 1:
        await display_game_menu(message, data["games"][0], edit=False, from_=None)

    else:
        await display_game_list(message, data, edit=False)


@router.callback_query(Transfer.filter(F.to_ == Screen.NOT_IMPLEMENTED))
async def not_implemented_callback(query: CallbackQuery):
    await query.answer("This button not implemented yet")


@router.callback_query(Transfer.filter(F.to_ == Screen.IGNORE))
async def ignored_callback(query: CallbackQuery):
    print("Entering ignored callback", flush=True)
    await query.answer(cache_time=60)


@router.callback_query()
async def not_handled_callback(query: CallbackQuery):
    print(f"Not handled callback: {query.data}", flush=True)
    await query.answer()
