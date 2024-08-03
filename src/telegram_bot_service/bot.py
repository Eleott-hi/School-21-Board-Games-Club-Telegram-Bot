from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from aiogram_dialog import setup_dialogs
from aiogram_dialog import DialogManager, StartMode

from ui.dialogs.game_dialog import dialog as game_dialog
from ui.dialogs.error_dialog import dialog as error_dialog
from ui.dialogs.profile_dialog import dialog as profile_dialog
from ui.dialogs.filters_dialog import dialog as filters_dialog
from ui.dialogs.settings_dialog import dialog as settings_dialog
from ui.dialogs.main_menu_dialog import dialog as main_menu_dialog
from ui.dialogs.pagination_dialog import dialog as pagination_dialog
from ui.dialogs.title_search_dialog import dialog as title_search_dialog
from ui.dialogs.registration_dialog import dialog as registration_dialog
from ui.dialogs.profile_booking_dialog import dialog as profile_booking_dialog
from ui.dialogs.profile_collection_dialog import dialog as profile_collection_dialog
from ui.dialogs.help_dialog import dialog as help_dialog
from ui.states import MainMenuSG, TelegramErrorSG
from core.Exceptions import TelegramException

from config import TELEGRAM_TOKEN
from database.database import database
from middlewares.MongoDB import UserMongoDB


async def on_startup(bot):
    print("The bot is alive")


async def on_shutdown(bot):
    print("The bot is dead")


# async def main() -> None:
bot = Bot(TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# await bot.delete_webhook(True)
dp = Dispatcher(db=database)
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

dp.update.middleware(UserMongoDB())


dp.include_routers(
    main_menu_dialog,
    pagination_dialog,
    profile_booking_dialog,
    profile_collection_dialog,
    game_dialog,
    filters_dialog,
    profile_dialog,
    settings_dialog,
    title_search_dialog,
    registration_dialog,
    help_dialog,
    error_dialog,
)
setup_dialogs(dp)


@dp.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.NORMAL)


@dp.error()
async def message_not_modified_handler(error_event, dialog_manager: DialogManager):
    print("Something went wrong:", error_event, flush=True)

    await error_event.update.callback_query.answer("Something went wrong")

    return True


# await dp.start_polling(bot)


# if __name__ == "__main__":
#     import logging, asyncio, sys

#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
