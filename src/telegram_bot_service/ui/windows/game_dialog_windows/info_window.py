from copy import deepcopy
from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia

from services.game_service import GameService
from core.Localization import Language, localization_manager
from ui.states import GameDialogSG


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["game_info_window"]
    common_text: Dict[str, str] = localization["common"]

    game: Dict = data["chosen_game"]

    return dict(
        title=window_text["title"].format_map(game),
        description=window_text["description"].format_map(game),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(
    aiogd_context,
    user_mongo: Dict,
    **kwargs,
):
    print(aiogd_context.start_data, flush=True)
    print(aiogd_context.dialog_data, flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    d_data = aiogd_context.dialog_data
    if "chosen_game" not in d_data:
        game: Dict = await GameService().get_game_by_id(d_data["game_id"])
        d_data["chosen_game"] = game

    return dict(
        text=text(d_data, user_mongo["options"]["language"]),
        photo=MediaAttachment(
            ContentType.PHOTO, url=d_data["chosen_game"]["photo_link"]
        ),
    )


window = Window(
    DynamicMedia("photo"),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    SwitchTo(
        Format("{text[back_button]}"),
        id="back",
        state=GameDialogSG.main,
    ),
    state=GameDialogSG.info,
    getter=getter,
)
