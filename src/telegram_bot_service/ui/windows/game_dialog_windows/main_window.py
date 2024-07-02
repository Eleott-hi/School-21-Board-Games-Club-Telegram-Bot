from copy import deepcopy
from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Row, Cancel, SwitchTo
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.api.entities.context import Context

from services.game_service import GameService
from core.Localization import Language, localization_manager
from ui.states import GameDialogSG
import ui.utils


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["game_menu_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        info_button=window_text["info_button"].format_map(data),
        booking_button=window_text["booking_button"].format_map(data),
        collection_button=window_text["collection_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
        back_to_main_menu_button=common_text["back_to_main_menu_button"].format_map(
            data
        ),
    )


async def getter(
    aiogd_context: Context,
    user_mongo: Dict,
    **kwargs,
):
    print(aiogd_context.start_data, flush=True)
    print(aiogd_context.dialog_data, flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    data = aiogd_context.dialog_data
    game: Dict = await GameService().get_game_by_id(data["game_id"])

    return dict(
        text=text({}, user_mongo["options"]["language"]),
        photo=MediaAttachment(ContentType.PHOTO, path=game["photo_link"]),
        game=game,
    )


window = Window(
    DynamicMedia("photo"),
    Format("{game[title]}"),
    Row(
        SwitchTo(
            Format("{text[info_button]}"),
            id="info",
            state=GameDialogSG.info,
        ),
        SwitchTo(
            Format("{text[booking_button]}"),
            id="booking",
            state=GameDialogSG.booking,
        ),
    ),
    Row(
        SwitchTo(
            Format("{text[collection_button]}"),
            id="collections",
            state=GameDialogSG.collections,
        ),
    ),
    Cancel(
        Format("{text[back_button]}"),
        id="cancel",
    ),
    ui.utils.default_back_to_main_menu_button(),
    state=GameDialogSG.main,
    getter=getter,
)
