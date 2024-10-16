from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Start, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.manager.manager import ManagerImpl


from ui.states import BookingSG, CollectionSG, OptionsSG, ProfileSG, RegistrationSG
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]

    window_text: Dict[str, str] = localization["profile_menu_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        booking_button=window_text["booking_button"].format_map(data),
        collections_button=window_text["collections_button"].format_map(data),
        registration_button=window_text["registration_button"].format_map(data),
        settings_button=window_text["settings_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(dialog_manager: ManagerImpl, user_mongo: Dict, **kwargs):
    user = dialog_manager.event.from_user

    text_data = dict(
        username=user.full_name if user else "Anonymous",
    )

    return dict(
        text=text(text_data, user_mongo["options"]["language"]),
        is_logged_in=user_mongo["options"]["is_logged_in"],
        is_not_logged_in=not user_mongo["options"]["is_logged_in"],
    )


window = Window(
    StaticMedia(
        path="resources/static/profile.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    Start(
        Format("{text[booking_button]}"),
        id="bookings",
        state=BookingSG.main,
        when="is_logged_in",
    ),
    Start(
        Format("{text[collections_button]}"),
        id="collections",
        state=CollectionSG.main,
        when="is_logged_in",
    ),
    Start(
        Format("{text[registration_button]}"),
        id="registration",
        state=RegistrationSG.start,
        when="is_not_logged_in",
    ),
    Start(
        Format("{text[settings_button]}"),
        id="options",
        state=OptionsSG.main,
    ),
    Cancel(
        Format("{text[back_button]}"),
        id="cancel",
    ),
    state=ProfileSG.main,
    getter=getter,
)
