import asyncio
from copy import deepcopy
import datetime
from datetime import date
from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType


from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import SwitchTo, ScrollingGroup, Button, Select
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.api.entities.context import Context

import ui.utils
from services.game_service import GameService
from services.booking_service import BookingService
from services.auth_service import AuthService
from ui.states import BookingSG, GameDialogSG, ProfileSG
from core.Localization import Language, localization_manager
from ui.widgets.CustomScrollingGroup import CustomScrollingGroup


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]

    window_text: Dict[str, str] = localization["profile_booking_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(
    aiogd_context: Context,
    dialog_manager: ManagerImpl,
    user_mongo: Dict,
    **kwargs,
):
    print("getter", aiogd_context, flush=True)
    d_data = aiogd_context.dialog_data

    if "user" not in d_data:
        user = await AuthService().get_user_by_telegram_id(user_mongo["_id"])
        d_data["user"] = user

    filters = {"user_id": d_data["user"].id, "from_date": date.today()}
    bookings = await BookingService().get_bookings(filters=filters)

    games_ids = set(map(lambda x: x["game_id"], bookings))
    tasks = [GameService().get_game_by_id(game_id) for game_id in games_ids]
    games = await asyncio.gather(*tasks)

    d_data["games"] = games

    print(d_data, flush=True)

    return dict(
        text=text({}, user_mongo["options"]["language"]),
        games=d_data["games"],
    )


async def on_game_selected(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
):
    d_data = manager.dialog_data
    d_data["game_id"] = item_id
    d_data["chosen_game"] = [g for g in d_data["games"] if g["id"] == item_id][0]

    await manager.start(
        state=GameDialogSG.booking,
        data=dict(
            user=d_data["user"],
            game_id=d_data["game_id"],
            chosen_game=d_data["chosen_game"],
        ),
    )


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
    CustomScrollingGroup(
        Select(
            Format("{item[title]}"),
            id="games",
            item_id_getter=lambda x: x["id"],
            items="games",
            on_click=on_game_selected,
        ),
        id="games_scrolling",
        height=5,
        width=1,
    ),
    ui.utils.default_back_button(),
    state=BookingSG.main,
    getter=getter,
)
