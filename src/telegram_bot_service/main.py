import asyncio
import logging
import sys

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from config import TELEGRAM_TOKEN
from keyboards.builders import inline_builder

from callbacks import navigations

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "main_menu")
async def command_start_handler(message: Message | CallbackQuery) -> None:
    keyboard = inline_builder(
        ["Лист"],
        ["list"],
    )

    answer = dict(
        text=f"Hello, {hbold(message.from_user.first_name)}!\n"
        "There is some menu",
        reply_markup=keyboard,
    )

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(**answer)
        await message.answer()
    else:
        await message.answer(**answer)


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        await message.answer(message.text)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_routers(
        router,
        navigations.router,
    )

    await bot.delete_webhook(True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
