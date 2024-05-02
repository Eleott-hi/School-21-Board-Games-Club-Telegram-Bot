from copy import deepcopy
import datetime
from math import ceil
from typing import Any, Dict

from aiogram.types import ContentType, CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window, StartMode
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import Cancel, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

from windows.option_windows.pagination_option_window import (
    window as pagination_option_window,
)
from windows.states import OptionsSG
from database.database import MDB
from aiogram_dialog.manager.manager import ManagerImpl
from core.Localization import localization


window_text = localization["settings_window"]
common_text = localization["common"]


def widget_from_user_options(options: Dict):
    return dict(
        pagination_limit=str(options["pagination_limit"]),
    )


async def get_data(dialog_manager: ManagerImpl, aiogd_context: Context, **kwargs):
    options = dialog_manager.middleware_data["user_mongo"]["options"]

    if not aiogd_context.widget_data:
        aiogd_context.widget_data = widget_from_user_options(options)

    print(options)

    return options


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/profile.jpg",
            type=ContentType.PHOTO,
        ),
        Multi(
            Const(window_text["title"]), Format(window_text["description"]), sep="\n\n"
        ),
        SwitchTo(
            Format(window_text["pagination_button"]),
            id="pagination",
            state=OptionsSG.pagination,
        ),
        Cancel(Const(common_text["back_button"]), id="cancel"),
        state=OptionsSG.main,
        getter=get_data,
    ),
    pagination_option_window,
)
