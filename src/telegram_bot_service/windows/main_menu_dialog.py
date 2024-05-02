from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Start, Group
from aiogram_dialog.widgets.text import Const, Multi
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia
from core.Localization import localization

from windows.states import (
    FilterSG,
    MainMenuSG,
    PaginationSG,
    ProfileSG,
    TitleSearchSG,
    not_implemented_yet,
)


async def goto_pagination(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    options = manager.middleware_data["user_mongo"]["options"]
    filters = dict(offset=0, limit=options["pagination_limit"])

    await manager.start(state=PaginationSG.main, data=filters)


window_text = localization["main_menu_window"]

dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        Multi(
            Const(window_text["title"]),
            Const(window_text["description"]),
            sep="\n\n",
        ),
        Button(
            Const(window_text["all_games_button"]),
            id="all_games",
            on_click=goto_pagination,
        ),
        Start(Const(window_text["filters_button"]), id="filters", state=FilterSG.main),
        Start(
            Const(window_text["title_search_button"]),
            id="title_search",
            state=TitleSearchSG.main,
        ),
        Start(Const(window_text["profile_button"]), id="profile", state=ProfileSG.main),
        Button(
            Const(window_text["help_button"]), id="help", on_click=not_implemented_yet
        ),
        state=MainMenuSG.main,
    ),
)
