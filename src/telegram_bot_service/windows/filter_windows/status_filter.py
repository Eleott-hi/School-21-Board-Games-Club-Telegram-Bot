from typing import Dict

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import ManagedRadio, SwitchTo, Column, Radio
from database.database import MDB

from windows.states import FilterSG


async def get_values(aiogd_context, user_mongo, **kwargs):
    return dict(status=["Any", "Available", "Unavailable"])


async def on_state_changed(
    cb: CallbackQuery,
    button: ManagedRadio,
    manager: ManagerImpl,
    value: str,
):

    db: MDB = manager.middleware_data["db"]
    user_mongo: Dict = manager.middleware_data["user_mongo"]

    curr_value = value if value != "Any" else None

    filter_name: str = "status"
    filters = user_mongo["optional_filters"]

    if filters[filter_name] != curr_value:
        filters[filter_name] = curr_value
        await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)


window = Window(
    StaticMedia(
        path="resources/static/filter.jpg",
        type=ContentType.PHOTO,
    ),
    Format("Select game status"),
    Column(
        Radio(
            Format("🔘 {item}"),
            Format("⚪️ {item}"),
            id="status",
            item_id_getter=str,
            items="status",
            on_state_changed=on_state_changed,
        )
    ),
    SwitchTo(Const("⬅️ Back"), id="to_game_menu", state=FilterSG.main),
    state=FilterSG.status,
    getter=get_values,
)
