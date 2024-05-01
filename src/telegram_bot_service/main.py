# import ngrok python sdk
import ngrok
from config import TELEGRAM_TOKEN
from fastapi import FastAPI
from bot import bot, dp, types, Dispatcher, Bot
import os
from typing import Dict


WEBHOOK_PATH = f"/bot/{TELEGRAM_TOKEN}"


async def lifespan(app):
    tmp = await ngrok.forward(8001, authtoken_from_env=True)
    forward_url = tmp.url()

    print(f"Forwarding established at {forward_url}")

    WEBHOOK_URL = f"{forward_url}{WEBHOOK_PATH}"

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=WEBHOOK_URL)

    yield

    print("Shutting down...")
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(f"{WEBHOOK_PATH}")
async def bot_webhook(update: types.Update):
    try:
        await dp.feed_update(bot=bot, update=update)
    except Exception as e: 
        print("Error processing update:", e)
        # dp.register_error_handler(bot, update)


@app.post(f"/notify")
async def notify_bot():
    await bot.send_message(chat_id=572276281, text="Hello from /send")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
