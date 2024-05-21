from typing import Any

from aiogram_dialog import DialogManager, ShowMode
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button


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
