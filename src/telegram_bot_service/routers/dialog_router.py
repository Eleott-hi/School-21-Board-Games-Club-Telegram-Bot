from typing import Any

from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Start, Group
from aiogram_dialog.widgets.text import Const
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia


class MySG(StatesGroup):
    first = State()


class SubDialogSG(StatesGroup):
    first = State()


async def main_process_result(
    start_data: Data, result: Any, dialog_manager: DialogManager
):
    print("We have result:", result)


dialog = Dialog(
    Window(
        Const("Main dialog"),
        Start(Const("Start 1"), id="start", state=SubDialogSG.first),
        state=MySG.first,
    ),
    on_process_result=main_process_result,
)


async def close_subdialog(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.done(result={"name": "Tishka17"})


subdialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        Const("Subdialog"),
        Button(Const("Close"), id="btn", on_click=close_subdialog),
        Cancel(Const("Close")),
        state=SubDialogSG.first,
    ),
)

dialogs = (dialog, subdialog)
