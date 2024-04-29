from copy import deepcopy
from math import ceil
from typing import Any, Dict

from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Start,
    Group,
    Row,
    Cancel,
    Next,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia


from windows.states import GameDialogSG, MainMenuSG, PaginationSG
from windows.states import not_implemented_yet, ignore
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select, Column
from aiogram_dialog.widgets.text import Const
import operator
from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format


# event
# middleware_data
# start_data
# dialog_data


async def next_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    print("event:", manager.event, flush=True)
    print("middleware_data:", manager.middleware_data, flush=True)
    print("start_data:", manager.start_data, flush=True)
    print("dialog_data:", manager.dialog_data, flush=True)

    next_offset = manager.dialog_data["offset"] + manager.dialog_data["limit"]

    if next_offset >= manager.dialog_data["total"]:
        await callback.answer("There are no more games")
        return

    manager.dialog_data["offset"] = next_offset
    await manager.show()


async def prev_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):

    prev_offset = max(0, manager.dialog_data["offset"] - manager.dialog_data["limit"])
    manager.dialog_data["offset"] = prev_offset
    await manager.show()


async def get_games(*, aiogd_context, **kwargs):
    print("getter", aiogd_context, flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    print(aiogd_context.dialog_data, flush=True)

    aiogd_context.dialog_data["total"] = 100

    gen = range(
        aiogd_context.dialog_data["offset"],
        aiogd_context.dialog_data["offset"] + aiogd_context.dialog_data["limit"],
    )

    return {
        "games": list(zip(gen, gen)),
        "total": aiogd_context.dialog_data["total"],
        "page": int(
            aiogd_context.dialog_data["offset"] / aiogd_context.dialog_data["limit"] + 1
        ),
        "pages": ceil(
            aiogd_context.dialog_data["total"] / aiogd_context.dialog_data["limit"]
        ),
        "prev": "⬅️",
        "next": "➡️",
    }


def here(**kwargs):
    print("here", flush=True)


async def on_game_selected(
    callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):

    data = dict(game_id=item_id)

    print()
    print("HERE")
    print()

    await manager.start(state=GameDialogSG.main, data=data)


async def go_to_first_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    manager.dialog_data["offset"] = 0

    await manager.show()


async def go_to_last_page(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    pages = ceil(manager.dialog_data["total"] / manager.dialog_data["limit"])

    manager.dialog_data["offset"] = (pages - 1) * manager.dialog_data["limit"]

    await manager.show()


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        Const("Pagination"),
        Column(
            Select(
                Format("{item[0]}"),
                id="s_fruits",
                item_id_getter=operator.itemgetter(0),
                items="games",
                on_click=on_game_selected,
            ),
        ),
        Row(
            Button(Const("1"), id="first_page", on_click=go_to_first_page),
            Button(Format("{prev}"), id="prev", on_click=prev_page),
            Button(Format("{page}/{pages}"), id="page", on_click=ignore),
            Button(Format("{next}"), id="next", on_click=next_page),
            Button(Format("{pages}"), id="last_page", on_click=go_to_last_page),
        ),
        Cancel(Const("⬅️ Back"), id="cancel"),
        state=PaginationSG.main,
        getter=get_games,
    ),
)
