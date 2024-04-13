from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.game_service import get_game_by_id
from routers.common import display_game_info, display_game_menu


router = Router()


def extract_id_from_callback_data(dropout_str: str = ""):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            query = args[0]
            id = query.data.replace(dropout_str, "").strip()
            res = await func(*args, id=id, **kwargs)

            return res

        return wrapper

    return decorator


@router.callback_query(F.data.regexp("game_menu_callback:"))
@extract_id_from_callback_data(dropout_str="game_menu_callback:")
async def game_menu_callback(query: CallbackQuery, id: str = None, **kwarg):
    message = query.message
    game = await get_game_by_id(id)
    await display_game_menu(
        message,
        game,
        edit=True,
        back_action={"buttons": ["⬅️ Back"], "callbacks": ["main_menu"]},
    )
    await query.answer()


@router.callback_query(F.data.regexp("game_info_callback:"))
@extract_id_from_callback_data(dropout_str="game_info_callback:")
async def game_info_callback(query: CallbackQuery, id: str = None, **kwarg):
    message = query.message
    game = await get_game_by_id(id)
    await display_game_info(message, game, edit=True)
    await query.answer()
