import asyncio

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    FSInputFile,
    InputMediaPhoto,
)
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from keyboards.builders import inline_builder, reply_builder

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    keyboard = inline_builder(
        ["All games", "Find with options"],
        ["list", "find_with_options"],
        one_time_keyboard=True,
    )
    answer = dict(
        photo=FSInputFile("resources/static/menu.jpg"),
        caption="Menu",
        reply_markup=keyboard,
    )

    await message.answer_photo(**answer)


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(query: CallbackQuery) -> None:
    message = query.message

    keyboard = inline_builder(
        ["All games", "Find with options"],
        ["list", "find_with_options"],
        one_time_keyboard=True,
    )

    answer = dict(
        media=InputMediaPhoto(
            media=FSInputFile("resources/static/menu.jpg"), caption="Menu"
        ),
        reply_markup=keyboard,
    )

    await message.edit_media(**answer)
