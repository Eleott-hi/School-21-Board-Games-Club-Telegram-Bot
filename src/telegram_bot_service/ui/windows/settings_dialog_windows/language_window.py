from typing import Any, Dict

from aiogram.types import ContentType, CallbackQuery
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.kbd import ManagedRadio, SwitchTo, Column, Radio

from database.database import MDB
from ui.states import OptionsSG
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["language_settings_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(user_mongo: Dict, **kwargs):
    data = [Language.EN.value, Language.RU.value]

    return dict(
        text=text({}, user_mongo["options"]["language"]),
        data=data,
    )


async def on_state_changed(
    cb: CallbackQuery,
    button: ManagedRadio,
    manager: ManagerImpl,
    value: str,
):
    value = Language(value)
    db: MDB = manager.middleware_data["db"]
    user: Dict = manager.middleware_data["user_mongo"]
    options: Dict = user["options"]

    tag: str = "language"

    if options[tag] != value:
        options[tag] = value
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
            id="language",
            item_id_getter=str,
            items="data",
            on_state_changed=on_state_changed,
        )
    ),
    SwitchTo(
        Format("{text[back_button]}"),
        id="to_game_menu",
        state=OptionsSG.main,
    ),
    state=OptionsSG.language,
    getter=getter,
)
