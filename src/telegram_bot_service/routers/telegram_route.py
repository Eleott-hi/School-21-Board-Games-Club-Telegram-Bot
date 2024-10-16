from fastapi import APIRouter
from bot import bot, dp, types
from config import TELEGRAM_TOKEN
from schemas.schemas import TelegramMessageToUser

router = APIRouter(
    prefix="/bot",
    tags=["Telegram Bot"],
)


@router.post(f"/{TELEGRAM_TOKEN}")
async def bot_webhook(update: types.Update):
    try:
        await dp.feed_update(bot=bot, update=update)
    except Exception as e:
        print("Error processing update:", e)


@router.post(f"/notify")
async def notify_bot(message: TelegramMessageToUser):
    await bot.send_message(chat_id=message.chat_id, text=message.text)
