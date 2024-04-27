from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram import types
from database.database import database

from config import TELEGRAM_TOKEN

from routers.routers import router

# from routers.filter_router import router as filter_router
# from routers.global_searcher import router as global_searcher_router
# from routers.calendar_router import router as calendar_router
from middlewares.MongoDB import UserMongoDB


# async def on_startup(bot):
#     print("The bot is alive")


# async def on_shutdown(bot):
#     print("The bot is dead")


bot = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher(db=database)
# dp.startup.register(on_startup)
# dp.shutdown.register(on_shutdown)

dp.update.middleware(UserMongoDB())

dp.include_routers(
    router,
    # filter_router,
    # calendar_router,
    # global_searcher_router,
)


# @dp.error()
# async def message_not_modified_handler(update):
#     print("Something went wrong:", update, flush=True)
#     return True


# await dp.start_polling(bot)


# if __name__ == "__main__":
#     import logging, asyncio, sys

#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
