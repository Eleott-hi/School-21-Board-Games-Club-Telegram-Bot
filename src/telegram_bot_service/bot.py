from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram import types
from database.database import database

from config import TELEGRAM_TOKEN

from windows.main_menu import dialog as main_menu_dialog, MainMenuSG
from windows.pagination import dialog as pagination_dialog
from windows.game_dialog import dialog as game_dialog
from windows.filters_dialog import dialog as filters_dialog
from windows.profile_dialog import dialog as profile_dialog

from middlewares.MongoDB import UserMongoDB

from aiogram_dialog import setup_dialogs

from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode


async def on_startup(bot):
    print("The bot is alive")


async def on_shutdown(bot):
    print("The bot is dead")


# async def main() -> None:
bot = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
# await bot.delete_webhook(True)
dp = Dispatcher(db=database)
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

dp.update.middleware(UserMongoDB())


dp.include_routers(
    main_menu_dialog,
    pagination_dialog,
    game_dialog,
    filters_dialog,
    profile_dialog,
)
setup_dialogs(dp)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.NORMAL)


@dp.error()
async def message_not_modified_handler(error_event):
    print("Something went wrong:", error_event, flush=True)

    error_event.update.callback_query.answer("Something went wrong")

    return True


# await dp.start_polling(bot)


# if __name__ == "__main__":
#     import logging, asyncio, sys

#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
