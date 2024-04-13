import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram import types


from config import TELEGRAM_TOKEN

from routers.search_router import router as search_router
from routers.menu_router import router as menu_router
from routers.option_router import router as option_router
from routers.global_searcher import router as global_searcher_router
from routers.game_menu_router import router as game_menu_router


async def on_startup(bot):
    print("The bot is alive")


async def on_shutdown(bot):
    print("The bot is dead")


# async def main() -> None:
bot = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
# await bot.delete_webhook(True)

dp = Dispatcher()
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)
dp.include_routers(
    menu_router,
    game_menu_router,
    search_router,
    option_router,
    global_searcher_router,
)

# await dp.start_polling(bot)


# if __name__ == "__main__":
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# asyncio.run(main())
