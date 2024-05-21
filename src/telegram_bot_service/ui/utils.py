from typing import Any
from aiogram_dialog import DialogManager, ShowMode


async def back_to_main_menu(
    manager: DialogManager,
    result: Any | None = None,
    show_mode: ShowMode | None = None,
):
    stack = manager.current_stack()
    intents = stack.intents
    stack.intents = [intents[0], intents[-1]]

    await manager.done(result=result, show_mode=show_mode)
