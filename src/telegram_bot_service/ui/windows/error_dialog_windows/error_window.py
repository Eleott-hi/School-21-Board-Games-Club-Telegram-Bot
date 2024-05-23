from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Cancel
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

import ui.utils
from ui.states import NotFoundSG
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]

    window_text: Dict[str, str] = localization["not_found_window"]
    common_text: Dict[str, str] = localization["common"]

    return {
        "title": window_text["title"].format_map(data),
        "description": window_text["description"].format_map(data),
        "back_button": common_text["back_button"].format_map(data),
        "back_to_main_menu_button": common_text["back_to_main_menu_button"].format_map(
            data
        ),
    }


async def getter(user_mongo: Dict, **kwargs):
    language = user_mongo["options"]["language"]

    return dict(
        text=text({}, language),
    )


window = Window(
    StaticMedia(
        path="resources/static/not_found.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    Cancel(Format("{text[back_button]}"), id="cancel"),
    Button(
        Format("{text[back_to_main_menu_button]}"),
        id="back_to_main_menu",
        on_click=ui.utils.default_on_back_to_main_menu,
    ),
    parse_mode="HTML",
    state=NotFoundSG.main,
    getter=getter,
)
