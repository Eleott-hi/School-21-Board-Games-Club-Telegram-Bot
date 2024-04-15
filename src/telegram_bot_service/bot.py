from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram import types
from database.database import database

from config import TELEGRAM_TOKEN

from routers.routers import router

from routers.filter_router import router as filter_router
from routers.global_searcher import router as global_searcher_router
from routers.calendar_router import router as calendar_router
from middlewares.MongoDB import UserMongoDB

# from routers.game_menu_router import router as game_menu_router


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
    router,
    filter_router,
    # game_menu_router,
    # search_router,
    # option_router,
    calendar_router,
    global_searcher_router,
)
# await dp.start_polling(bot)


# if __name__ == "__main__":
#     import logging, asyncio, sys

#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
