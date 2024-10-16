from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Format, Multi

from core.Exceptions import TelegramException
from ui.states import TelegramErrorSG


async def back_to_main_menu(
    manager: DialogManager,
    result: Any | None = None,
    show_mode: ShowMode | None = None,
):
    stack = manager.current_stack()
    stack.intents = [stack.intents[0], stack.intents[-1]]

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


def default_back_button():
    return Cancel(
        Format("{text[back_button]}"),
        id="cancel",
    )


def telegram_error_handling_decorator(func):
    async def wrapper(*args, **kwargs):
        manager: DialogManager = args[2]

        try:
            print("HERE", type(manager), flush=True)
            await func(*args, **kwargs)

        except TelegramException as e:
            await manager.start(TelegramErrorSG.main, data=dict(error=e))

    return wrapper
