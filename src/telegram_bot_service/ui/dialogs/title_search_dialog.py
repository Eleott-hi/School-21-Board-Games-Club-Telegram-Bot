from typing import Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types.message import Message
from aiogram_dialog.manager.manager import ManagerImpl

from services.game_service import GameService
from ui.states import GameDialogSG, NotFoundSG, PaginationSG, TitleSearchSG
from database.database import MDB

from core.Localization import localization

window_text = localization["title_search_menu_window"]
common_text = localization["common"]


async def getter(aiogd_context, db: MDB, user_mongo: Dict, **kwargs):
    print("aiogd_context", aiogd_context, flush=True)
    print("user_mongo", user_mongo, flush=True)

    if not aiogd_context.widget_data:
        aiogd_context.widget_data = dict(
            location="Title",
            input="",
        )

    data = aiogd_context.widget_data

    return data


async def goto(callback: CallbackQuery, button: Button, manager: DialogManager):
    data = manager.current_context().widget_data
    options = manager.middleware_data["user_mongo"]["options"]

    filters = dict(offset=0, limit=options["pagination_limit"], title=data["input"])

    games = await GameService.get_games(filters)

    if games["total"] == 0:
        await manager.start(NotFoundSG.main)

    elif games["total"] == 1:
        game_id = games["games"][0]["id"]
        await manager.start(GameDialogSG.main, data=dict(game_id=game_id))

    else:
        await manager.start(PaginationSG.main, data=filters)


async def reset_filters(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    manager.current_context().widget_data = dict(
        location="Title",
        input="",
    )

    await manager.show()


async def user_input_text(message: Message, b: MessageInput, manager: ManagerImpl):
    print(message.text, flush=True)

    manager.current_context().widget_data["input"] = message.text


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/filter.jpg",
            type=ContentType.PHOTO,
        ),
        Multi(
            Const(window_text["title"]),
            Multi(
                Const(window_text["description"]),
                Format(window_text["current_input"]),
            ),
            sep="\n\n",
        ),
        MessageInput(user_input_text, content_types=ContentType.TEXT),
        Row(
            Button(
                Const(window_text["reset_button"]), id="reset", on_click=reset_filters
            ),
            Button(
                Const(window_text["search_button"]),
                id="search",
                on_click=goto,
            ),
        ),
        Cancel(Const(common_text["back_to_main_menu_button"]), id="cancel"),
        state=TitleSearchSG.main,
        parse_mode="HTML",
        getter=getter,
    ),
)
