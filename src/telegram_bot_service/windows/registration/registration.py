from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types.message import Message
from aiogram_dialog.manager.manager import ManagerImpl

from services.auth_service import AuthService
from windows.states import NotFoundSG, RegistrationSG, ignore
from database.database import MDB

from core.Localization import localization


window_text = localization["registration_window"]
common_text = localization["common"]


async def getter(aiogd_context, db: MDB, user_mongo: Dict, **kwargs):
    if not aiogd_context.widget_data:
        aiogd_context.widget_data = dict(
            input="",
        )

    data = aiogd_context.widget_data
    return data


async def register(callback: CallbackQuery, button: Button, manager: DialogManager):
    nickname = manager.current_context().widget_data["input"]
    if nickname is None:
        return

    auth = AuthService()
    telegram_id = callback.from_user.id
    success = await auth.register(nickname, telegram_id)

    if not success:
        await manager.start(NotFoundSG.main)
        return

    manager.current_context().widget_data["input"] = ""
    await manager.switch_to(RegistrationSG.confirm)


async def user_input_text(message: Message, b: MessageInput, manager: ManagerImpl):
    print(message.text, flush=True)
    manager.current_context().widget_data["input"] = message.text


window = Window(
    StaticMedia(
        path="resources/static/profile.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Const(window_text["title"]),
        Multi(
            Const(window_text["description"]),
            Format(window_text["current_input"]),
        ),
        sep="\n\n",
    ),
    Button(
        Const(window_text["register_button"]),
        id="register",
        on_click=register,
    ),
    MessageInput(user_input_text, content_types=ContentType.TEXT),
    Cancel(Const(common_text["back_button"]), id="cancel"),
    state=RegistrationSG.start,
    parse_mode="HTML",
    getter=getter,
)
