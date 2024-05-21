import ngrok
from config import TELEGRAM_TOKEN
from fastapi import FastAPI
from bot import bot
from routers.telegram_route import router as telegram_router


async def lifespan(app):
    tmp = await ngrok.forward(8000, authtoken_from_env=True)
    forward_url = tmp.url()

    print(f"Forwarding established at {forward_url}")

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=f"{forward_url}/bot/{TELEGRAM_TOKEN}")

    yield

    print("Shutting down...")
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(telegram_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
