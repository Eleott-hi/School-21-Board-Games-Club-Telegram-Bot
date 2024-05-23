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

from ui.states import GameDialogSG, PaginationSG, NotFoundSG, ignore
from services.game_service import GameService
from core.Localization import localization_manager


def text(data: Dict, language: str) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text = localization["pagination_window"]
    common_text = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        first_page_button=window_text["first_page_button"].format_map(data),
        prev_button=window_text["prev_button"].format_map(data),
        pagination_info=window_text["pagination_info"].format_map(data),
        next_button=window_text["next_button"].format_map(data),
        last_page_button=window_text["last_page_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
        #
        no_pages_message=window_text["no_pages_message"].format_map(data),
    )


async def getter(
    aiogd_context: Context,
    dialog_manager: ManagerImpl,
    user_mongo: Dict,
    **kwargs,
):
    print("getter", aiogd_context, flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = dict(
            filters=deepcopy(aiogd_context.start_data),
            data={},
            utils={},
        )

    data = aiogd_context.dialog_data["data"]
    filters = aiogd_context.dialog_data["filters"]
    utils = aiogd_context.dialog_data["utils"]

    games_info: Dict = await GameService.get_games(filters)
    data["games"] = games_info["games"]
    data["total"] = games_info["total"]

    if data["total"] == 0:
        dialog_manager.current_stack().pop()
        await dialog_manager.start(state=NotFoundSG.main)
        return

    text_data = dict(
        pages=ceil(data["total"] / filters["limit"]),
        page=int(filters["offset"] / filters["limit"] + 1),
    )

    _text = text(text_data, user_mongo["options"]["language"])
    utils["no_pages_message"] = _text["no_pages_message"]

    return dict(
        text=_text,
        games=data["games"],
    )


async def on_game_selected(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
):
    await manager.start(state=GameDialogSG.main, data=dict(game_id=item_id))


async def prev_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    filters = manager.dialog_data["filters"]
    utils = manager.dialog_data["utils"]

    prev_offset = filters["offset"] - filters["limit"]

    if prev_offset < 0:
        await callback.answer(utils["no_pages_message"])
        return

    filters["offset"] = prev_offset
    await manager.show()


async def next_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    filters = manager.dialog_data["filters"]
    data = manager.dialog_data["data"]
    utils = manager.dialog_data["utils"]

    next_offset = filters["offset"] + filters["limit"]

    if next_offset >= data["total"]:
        await callback.answer(utils["no_pages_message"])
        return

    filters["offset"] = next_offset
    await manager.show()


async def goto_first_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    filters = manager.dialog_data["filters"]
    filters["offset"] = 0

    await manager.show()


async def goto_last_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    filters = manager.dialog_data["filters"]
    data = manager.dialog_data["data"]

    pages = ceil(data["total"] / filters["limit"])
    filters["offset"] = (pages - 1) * filters["limit"]

    await manager.show()


window = Window(
    StaticMedia(
        path="resources/static/menu.jpg",
        type=ContentType.PHOTO,
    ),
    Format("{text[title]}"),
    Column(
        Select(
            Format("{item[title]}"),
            id="s_fruits",
            item_id_getter=lambda x: x["id"],
            items="games",
            on_click=on_game_selected,
        ),
    ),
    Row(
        Button(
            Format("{text[first_page_button]}"),
            id="first_page",
            on_click=goto_first_page,
        ),
        Button(
            Format("{text[prev_button]}"),
            id="prev",
            on_click=prev_page,
        ),
        Button(
            Format("{text[pagination_info]}"),
            id="page",
            on_click=ignore,
        ),
        Button(
            Format("{text[next_button]}"),
            id="next",
            on_click=next_page,
        ),
        Button(
            Format("{text[last_page_button]}"),
            id="last_page",
            on_click=goto_last_page,
        ),
    ),
    Cancel(Format("{text[back_button]}"), id="cancel"),
    state=PaginationSG.main,
    getter=getter,
)
