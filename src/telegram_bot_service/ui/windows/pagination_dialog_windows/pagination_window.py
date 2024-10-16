import operator

from typing import Any, Dict
from copy import deepcopy
from math import ceil

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Select, Column

import ui.utils
from ui.widgets.CustomScrollingGroup import CustomScrollingGroup
from ui.states import GameDialogSG, PaginationSG, TelegramErrorSG, ignore
from services.game_service import GameService
from core.Localization import localization_manager


def text(data: Dict, language: str) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text = localization["pagination_window"]
    common_text = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
        back_to_main_menu_button=common_text["back_to_main_menu_button"].format_map(
            data,
        ),
    )


async def getter(
    aiogd_context: Context,
    dialog_manager: ManagerImpl,
    user_mongo: Dict,
    **kwargs,
):
    print("getter", aiogd_context, flush=True)

    s_data = aiogd_context.start_data
    d_data = aiogd_context.dialog_data

    if not d_data:
        d_data.update(**deepcopy(s_data))

    if "games" not in d_data:
        raise ValueError("Games not in d_data")

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

    game = [g for g in d_data["games"] if g["id"] == item_id][0]

    await manager.start(
        state=GameDialogSG.main,
        data=dict(chosen_game=game),
    )


window = Window(
    StaticMedia(
        path="resources/static/menu.jpg",
        type=ContentType.PHOTO,
    ),
    Format("{text[title]}"),
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
    Cancel(Format("{text[back_button]}"), id="cancel"),
    ui.utils.default_back_to_main_menu_button(),
    state=PaginationSG.main,
    getter=getter,
)
