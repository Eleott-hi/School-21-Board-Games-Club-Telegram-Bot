from copy import deepcopy
from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia

import ui.utils
from services.game_service import GameService
from core.Localization import Language, localization_manager
from ui.states import HelpSG


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["help_dialog_main_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(
    aiogd_context,
    user_mongo: Dict,
    **kwargs,
):
    return dict(
        text=text(dict(), user_mongo["options"]["language"]),
    )


window = Window(
    StaticMedia(
        path="resources/static/menu.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    ui.utils.default_back_button(),
    state=HelpSG.main,
    getter=getter,
)
