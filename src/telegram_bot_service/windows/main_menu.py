from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Start, Group
from aiogram_dialog.widgets.text import Const
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia


from windows.states import FilterSG, MainMenuSG, PaginationSG, not_implemented_yet


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        Const("Main menu"),
        Start(
            Const("Games"),
            id="all_games",
            state=PaginationSG.main,
            data={"offset": 0, "limit": 10},
        ),
        Start(Const("Filters"), id="filters", state=FilterSG.main),
        Button(Const("Profile"), id="profile", on_click=not_implemented_yet),
        Button(Const("Help"), id="help", on_click=not_implemented_yet),
        state=MainMenuSG.main,
    ),
)
