from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery


init_user_dict: Dict = {
    "optional_filters": dict(
        age=None,
        status=None,
        players_num=None,
        duration=None,
        complexity=None,
        genres=[],
    )
}


class UserMongoDB(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        db = data["db"]

        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
        else:
            print(event, flush=True)
            raise Exception("Unknown event type")

        user = await db.users.find_one({"_id": user_id})

        if not user:
            await db.users.insert_one({"_id": user_id, **init_user_dict})
            user = await db.users.find_one({"_id": user_id})

        data["user_mongo"] = user

        print(user)

        return await handler(event, data)
