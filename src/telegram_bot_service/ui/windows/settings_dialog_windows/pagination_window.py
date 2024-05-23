from typing import Any, Dict

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import ManagedRadio, SwitchTo, Column, Radio

from ui.states import OptionsSG
from database.database import MDB
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text = localization["pagination_option_window"]
    common_text = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(user_mongo: Dict, **kwargs):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return dict(
        text=text({}, user_mongo["options"]["language"]),
        pagination_limits=data,
    )


async def process_event(
    cb: CallbackQuery,
    button: ManagedRadio,
    manager: ManagerImpl,
    value: str,
):
    value = int(value)

    db: MDB = manager.middleware_data["db"]
    user: Dict = manager.middleware_data["user_mongo"]
    options = user["options"]

    filter_name: str = "pagination_limit"

    if options[filter_name] != value:
        options[filter_name] = value
        await db.users.replace_one({"_id": user["_id"]}, user)


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
        Radio(
            Format("🔘 {item}"),
            Format("⚪️ {item}"),
            id="pagination_limit",
            item_id_getter=str,
            items="pagination_limits",
            on_state_changed=process_event,
        )
    ),
    SwitchTo(
        Format("{text[back_button]}"),
        id="to_game_menu",
        state=OptionsSG.main,
    ),
    state=OptionsSG.pagination,
    getter=getter,
)
