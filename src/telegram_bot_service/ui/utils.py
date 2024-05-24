from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Multi


async def back_to_main_menu(
    manager: DialogManager,
    result: Any | None = None,
    show_mode: ShowMode | None = None,
):
    stack = manager.current_stack()
    intents = stack.intents
    stack.intents = [intents[0], intents[-1]]

    await manager.done(result=result, show_mode=show_mode)


def default_on_back_to_main_menu(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    return back_to_main_menu(manager)


def default_back_to_main_menu_button():
    return Button(
        Format("{text[back_to_main_menu_button]}"),
        id="back_to_main_menu",
        on_click=default_on_back_to_main_menu,
    )
