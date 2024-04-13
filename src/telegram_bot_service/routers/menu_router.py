import asyncio

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from routers.common import display_main_menu

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await display_main_menu(message, edit=False)


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(query: CallbackQuery) -> None:
    message = query.message
    await display_main_menu(message, edit=True)
    await query.answer()
