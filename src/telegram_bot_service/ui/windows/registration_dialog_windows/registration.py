from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType
from aiogram.types.message import Message

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.manager.manager import ManagerImpl

from services.auth_service import AuthService
from ui.states import TelegramErrorSG, RegistrationSG
from database.database import MDB

from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["registration_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        current_input=window_text["current_input"].format_map(data),
        register_button=window_text["register_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(aiogd_context, user_mongo: Dict, **kwargs):
    if not aiogd_context.widget_data:
        aiogd_context.widget_data = dict(
            input="",
        )

    data = aiogd_context.widget_data

    return dict(
        text=text(data, user_mongo["options"]["language"]),
    )


async def register(callback: CallbackQuery, button: Button, manager: DialogManager):
    nickname = manager.current_context().widget_data["input"]
    if nickname is None:
        return

    auth = AuthService()
    telegram_id = callback.from_user.id
    success = await auth.register(nickname, telegram_id)

    if not success:
        await manager.start(TelegramErrorSG.main)
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
        Format("{text[title]}"),
        Multi(
            Format("{text[description]}"),
            Format("{text[current_input]}"),
        ),
        sep="\n\n",
    ),
    Button(
        Format("{text[register_button]}"),
        id="register",
        on_click=register,
    ),
    MessageInput(
        user_input_text,
        content_types=ContentType.TEXT,
    ),
    Cancel(
        Format("{text[back_button]}"),
        id="cancel",
    ),
    state=RegistrationSG.start,
    parse_mode="HTML",
    getter=getter,
)
