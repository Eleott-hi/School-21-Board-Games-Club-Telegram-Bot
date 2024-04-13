from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.game_service import get_game_by_id
from routers.common import display_game_info, display_game_menu
from callbacks.callback_data import GameBooking, GameInfo, GameMenu

router = Router()


@router.callback_query(GameMenu.filter())
async def game_menu_callback(query: CallbackQuery, callback_data: GameMenu):
    message = query.message
    game = await get_game_by_id(callback_data.id)
    await display_game_menu(message, game, page=callback_data.page, edit=True)
    await query.answer()


@router.callback_query(GameInfo.filter())
async def game_info_callback(query: CallbackQuery, callback_data: GameInfo):
    message = query.message
    game = await get_game_by_id(callback_data.id)
    await display_game_info(message, game, edit=True)
    await query.answer()


@router.callback_query(GameBooking.filter())
async def game_booking_callback(query: CallbackQuery, callback_data: GameBooking):
    message = query.message
    await query.answer()
