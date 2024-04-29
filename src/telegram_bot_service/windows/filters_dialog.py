from copy import deepcopy
import datetime
from math import ceil
from typing import Any, Dict

from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Start,
    Group,
    Row,
    Cancel,
    Next,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia


from windows.states import MainMenuSG, PaginationSG, FilterSG
from windows.states import not_implemented_yet, ignore
from aiogram_dialog.widgets.kbd import (
    Button,
    ScrollingGroup,
    Select,
    Column,
    CalendarConfig,
)
from aiogram_dialog.widgets.text import Const
import operator
from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Radio, Multiselect
from aiogram_dialog.widgets.text import Format
from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from typing import Dict

from aiogram_dialog import DialogManager


from aiogram_dialog.widgets.text import Const, Format
from windows.filter_windows.age_window import window as age_window
from windows.filter_windows.genre_window import window as genre_window
from windows.filter_windows.players_filter import window as players_filter
from windows.filter_windows.complexity_filter import window as complexity_filter

# from windows.filter_windows.rating_filter import window as rating_filter
from windows.filter_windows.duration_filter import window as duration_filter
from windows.filter_windows.status_filter import window as status_filter

from database.database import MDB


def get_filters_from_user_mongo(user_mongo: Dict) -> Dict[str, Any]:
    filters: Dict[str, Any] = user_mongo["optional_filters"]
    filters = {key: value if value else "Any" for key, value in filters.items()}

    if filters["genres"] == "Any":
        filters["genres"] = [filters["genres"]]

    return filters


async def get_filter(aiogd_context, db: MDB, user_mongo: Dict, **kwargs):
    print("getter", flush=True)
    print("aiogd_context", aiogd_context, flush=True)
    print("user_mongo", user_mongo, flush=True)

    filters: Dict[str, Any] = get_filters_from_user_mongo(user_mongo)

    if not aiogd_context.widget_data:
        aiogd_context.widget_data = filters

    return {**filters, "genres": ", ".join(filters["genres"])}


async def goto_pagination(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    filters = manager.middleware_data["user_mongo"]["optional_filters"]
    # await manager.mark_closed()
    await manager.start(
        PaginationSG.main,
        data=dict(offset=0, limit=10, **filters),
    )


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/filter.jpg",
            type=ContentType.PHOTO,
        ),
        # Format("{title} {id}"),
        SwitchTo(
            Format("Genre: {genres}"), id="genre", state=FilterSG.genre
        ),
        SwitchTo(Format("Age: {age}"), id="age", state=FilterSG.age),
        SwitchTo(
            Format("Players: {players_num}"),
            id="players_num",
            state=FilterSG.players_num,
        ),
        SwitchTo(
            Format("Duration: {duration}"), id="duration", state=FilterSG.duration
        ),
        SwitchTo(
            Format("Complexity: {complexity}"),
            id="complexity",
            state=FilterSG.complexity,
        ),
        SwitchTo(Format("Status: {status}"), id="status", state=FilterSG.status),
        Button(Const("🔎 Search"), id="search", on_click=goto_pagination),
        Cancel(Const("⬅️ Back to menu"), id="cancel"),
        state=FilterSG.main,
        getter=get_filter,
    ),
    genre_window,
    age_window,
    players_filter,
    duration_filter,
    complexity_filter,
    status_filter,
)
