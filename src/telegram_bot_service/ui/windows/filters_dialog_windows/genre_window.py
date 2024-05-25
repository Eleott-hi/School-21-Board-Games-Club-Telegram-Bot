from typing import Any, Dict, List

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import (
    ManagedRadio,
    SwitchTo,
    Column,
    Multiselect,
    ManagedMultiselect,
)
from database.database import MDB

from ui.states import FilterSG
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text = localization["genre_filter_window"]
    common_text = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(user_mongo: Dict, **kwargs):
    return dict(
        text=text({}, user_mongo["options"]["language"]),
        genres=["Any", "Strategy", "RPG", "War", "Shooter", "Sports"],
    )


async def on_click(
    cb: CallbackQuery, widget: ManagedMultiselect, manager: ManagerImpl, value: Any
):
    print(value, flush=True)

    if value == "Any":
        await widget.reset_checked()
    else:
        curr_values = widget.get_checked()
        await widget.set_checked("Any", checked=curr_values == [value])


async def on_state_changed(
    cb: CallbackQuery, widget: ManagedRadio, manager: ManagerImpl, value: str
):
    db: MDB = manager.middleware_data["db"]
    user_mongo: Dict = manager.middleware_data["user_mongo"]

    curr_values: List = widget.get_checked()
    curr_values = [] if curr_values == ["Any"] else curr_values

    filter_name: str = "genres"
    filters: List | None = user_mongo["optional_filters"]

    if len(filters[filter_name] or []) != len(curr_values):
        filters[filter_name] = curr_values or None
        await db.users.replace_one({"_id": user_mongo["_id"]}, user_mongo)


window = Window(
    StaticMedia(
        path="resources/static/filter.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    Column(
        Multiselect(
            Format("✅ {item}"),
            Format("☑️ {item}"),
            id="genres",
            item_id_getter=lambda x: x,
            items="genres",
            on_click=on_click,
            on_state_changed=on_state_changed,
        )
    ),
    SwitchTo(
        Format("{text[back_button]}"),
        id="to_game_menu",
        state=FilterSG.main,
    ),
    state=FilterSG.genre,
    getter=getter,
)
