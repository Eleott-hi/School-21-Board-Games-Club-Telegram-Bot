from typing import Dict

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import ManagedRadio, SwitchTo, Column, Radio
from database.database import MDB

from ui.states import FilterSG
from core.Localization import localization

window_text = localization["complexity_filter_window"]
common_text = localization["common"]


async def getter(
    aiogd_context,
    user_mongo,
    **kwargs,
):
    return dict(complexity=["Any", "Easy", "Medium", "Hard"])


async def on_state_changed(
    cb: CallbackQuery,
    button: ManagedRadio,
    manager: ManagerImpl,
    value: str,
):

    db: MDB = manager.middleware_data["db"]
    user_mongo: Dict = manager.middleware_data["user_mongo"]

    curr_value = value if value != "Any" else None

    filter_name: str = "complexity"
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
        sep="\n\n",
    ),
    Column(
        Radio(
            Format("🔘 {item}"),
            Format("⚪️ {item}"),
            id="complexity",
            item_id_getter=str,
            items="complexity",
            on_state_changed=on_state_changed,
        )
    ),
    SwitchTo(Const(common_text["back_button"]), id="to_game_menu", state=FilterSG.main),
    state=FilterSG.complexity,
    getter=getter,
)
