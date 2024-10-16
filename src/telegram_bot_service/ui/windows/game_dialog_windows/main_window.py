from copy import deepcopy
from typing import Any, Dict

from aiogram.types import ContentType

from magic_filter import F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Cancel, Row, Cancel, SwitchTo, Start
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.api.entities.context import Context

from services.game_service import GameService
from core.Localization import Language, localization_manager
from ui.states import GameDialogSG, RegistrationSG
from ui.widgets.CustomDynamicMedia import CustomDynamicMedia
import ui.utils


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["game_menu_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        info_button=window_text["info_button"].format_map(data),
        booking_button=window_text["booking_button"].format_map(data),
        collection_button=window_text["collection_button"].format_map(data),
        register_button=window_text["register_button"].format_map(data),
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
    s_data = aiogd_context.start_data
    d_data = aiogd_context.dialog_data

    if not d_data:
        d_data.update(**deepcopy(s_data))

    if "chosen_game" not in d_data:
        game: Dict = await GameService().get_game_by_id(d_data["game_id"])
        d_data["chosen_game"] = game

    media = MediaAttachment(ContentType.PHOTO, url=d_data["chosen_game"]["photo_link"])

    print(media.url, flush=True)
    
    return dict(
        text=text({}, user_mongo["options"]["language"]),
        photo=media,
        game=d_data["chosen_game"],
        is_logged_in=user_mongo["options"]["is_logged_in"],
        is_not_logged_in=not user_mongo["options"]["is_logged_in"],
    )


window = Window(
    CustomDynamicMedia("photo"),
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
            when="is_logged_in",
        ),
    ),
    SwitchTo(
        Format("{text[collection_button]}"),
        id="collections",
        state=GameDialogSG.collections,
        when="is_logged_in",
    ),
    Start(
        Format("{text[register_button]}"),
        id="register",
        state=RegistrationSG.start,
        when="is_not_logged_in",
    ),
    Cancel(
        Format("{text[back_button]}"),
        id="cancel",
    ),
    ui.utils.default_back_to_main_menu_button(),
    state=GameDialogSG.main,
    getter=getter,
)
