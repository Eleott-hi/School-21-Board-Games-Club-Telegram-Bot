from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import StaticMedia

from ui.states import ProfileSG
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(user_mongo: Dict, **kwargs):
    return dict(
        text=text({}, user_mongo["options"]["language"]),
    )


window = Window(
    StaticMedia(
        path="resources/static/profile.jpg",
        type=ContentType.PHOTO,
    ),
    Const("Here is your collections"),
    SwitchTo(
        Format("{text[back_button]}"),
        id="cancel",
        state=ProfileSG.main,
    ),
    state=ProfileSG.collections,
    getter=getter,
)
