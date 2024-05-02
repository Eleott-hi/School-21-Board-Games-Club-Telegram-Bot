from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

from windows.states import NotFoundSG
from core.Localization import localization

window_text = localization["not_found_window"]
common_text = localization["common"]


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/not_found.jpg",
            type=ContentType.PHOTO,
        ),
        Multi(
            Const(window_text["title"]),
            Const(window_text["description"]),
            sep="\n\n",
        ),
        Cancel(Const(common_text["back_button"]), id="cancel"),
        parse_mode="HTML",
        state=NotFoundSG.main,
    ),
)
