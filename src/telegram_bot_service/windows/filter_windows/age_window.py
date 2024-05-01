import operator
from copy import deepcopy
from math import ceil
from typing import Any, Dict

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Data, Dialog, DialogManager, Window, ChatEvent
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import (
    Checkbox,
    ManagedCheckbox,
    ManagedRadio,
    Start,
    Group,
    Row,
    Cancel,
    Next,
    SwitchTo,
    Button,
    ScrollingGroup,
    Select,
    Column,
    CalendarConfig,
    Radio,
    Multiselect,
)
from database.database import MDB

from windows.states import FilterSG, not_implemented_yet, ignore

from core.Localization import localization

window_text = localization["age_filter_window"]
common_text = localization["common"]


async def get_ages(aiogd_context, user_mongo, **kwargs):
    return dict(ages=["Any", "5+", "10+", "18+"])


# <class 'aiogram.types.callback_query.CallbackQuery'>
# <class 'aiogram_dialog.widgets.kbd.select.ManagedRadio'>
# <class 'aiogram_dialog.manager.manager.ManagerImpl'>
# <class 'str'>


async def on_state_changed(
    cb: CallbackQuery,
    button: ManagedRadio,
    manager: ManagerImpl,
    value: str,
):

    db: MDB = manager.middleware_data["db"]
    user_mongo: Dict = manager.middleware_data["user_mongo"]

    curr_value = value if value != "Any" else None

    filter_name: str = "age"
    filters = user_mongo["optional_filters"]

    if filters[filter_name] != curr_value:
        filters[filter_name] = curr_value
        await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)


window = Window(
    StaticMedia(
        path="resources/static/filter.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Const(window_text["title"]),
        Const(window_text["description"]),
    ),
    Column(
        Radio(
            Format("🔘 {item}"),
            Format("⚪️ {item}"),
            id="age",
            item_id_getter=str,
            items="ages",
            on_state_changed=on_state_changed,
        )
    ),
    SwitchTo(Const(common_text["back_button"]), id="to_game_menu", state=FilterSG.main),
    state=FilterSG.age,
    getter=get_ages,
)
