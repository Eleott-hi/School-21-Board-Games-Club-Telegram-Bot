import asyncio
from copy import deepcopy
import datetime
from datetime import date
from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType


from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import SwitchTo, ScrollingGroup, Button, Select, Row
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.api.entities.context import Context

import ui.utils
from services.game_service import GameService
from services.collection_service import CollectionService, CollectionType
from services.booking_service import BookingService
from services.auth_service import AuthService, User
from ui.states import CollectionSG, GameDialogSG, ProfileSG, not_implemented_yet
from core.Localization import Language, localization_manager
from ui.widgets.CustomScrollingGroup import CustomScrollingGroup


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]

    window_text: Dict[str, str] = localization["profile_collection_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        favorite_button=window_text["favorite_button"].format_map(data),
        black_list_button=window_text["black_list_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
        back_to_main_menu_button=common_text["back_to_main_menu_button"].format_map(
            data
        ),
    )


async def prepare(s_data: Dict, d_data: Dict, user_mongo: Dict):
    if "user" not in d_data:
        user: User = await AuthService().get_user_by_telegram_id(user_mongo["_id"])
        d_data["user"] = user


async def getter(
    aiogd_context: Context,
    dialog_manager: ManagerImpl,
    user_mongo: Dict,
    **kwargs,
):
    s_data = aiogd_context.start_data
    d_data = aiogd_context.dialog_data

    await prepare(s_data, d_data, user_mongo)

    return dict(
        text=text({}, user_mongo["options"]["language"]),
    )


async def to_favorite_list(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    d_data = manager.dialog_data
    d_data["collection_type"] = CollectionType.FAVORITE

    await manager.switch_to(state=CollectionSG.pagination)


async def to_black_list(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    d_data = manager.dialog_data
    d_data["collection_type"] = CollectionType.BLACK_LIST

    await manager.switch_to(state=CollectionSG.pagination)


window = Window(
    StaticMedia(
        path="resources/static/profile.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    Row(
        Button(
            Format("{text[favorite_button]}"),
            id="favorite_button",
            on_click=to_favorite_list,
        ),
        Button(
            Format("{text[black_list_button]}"),
            id="black_list_button",
            on_click=to_black_list,
        ),
    ),
    ui.utils.default_back_button(),
    ui.utils.default_back_to_main_menu_button(),
    state=CollectionSG.main,
    getter=getter,
)
