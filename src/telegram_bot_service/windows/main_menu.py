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
    not_implemented_yet,
)

from config import PAGINATION_LIMIT

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
    ),
        Start(
            Const(window_text["all_games_button"]),
            id="all_games",
            state=PaginationSG.main,
            data={"offset": 0, "limit": PAGINATION_LIMIT},
        ),
        Start(Const(window_text["filters_button"]), id="filters", state=FilterSG.main),
        Start(Const(window_text["profile_button"]), id="profile", state=ProfileSG.main),
        Button(
            Const(window_text["help_button"]), id="help", on_click=not_implemented_yet
        ),
        state=MainMenuSG.main,
    ),
)
