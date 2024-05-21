from typing import Any, Dict

from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import Cancel, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

from ui.states import OptionsSG
from core.Localization import Language, localization_manager


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["settings_window"]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        pagination_button=window_text["pagination_button"].format_map(data),
        language_button=window_text["language_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(user_mongo: Dict, aiogd_context: Context, **kwargs):
    options = user_mongo["options"]

    if not aiogd_context.widget_data:
        aiogd_context.widget_data = dict(
            pagination_limit=str(options["pagination_limit"]),
            language=str(options["language"]),
        )

    return dict(
        text=text(options, options["language"]),
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
    SwitchTo(
        Format("{text[pagination_button]}"),
        id="pagination",
        state=OptionsSG.pagination,
    ),
    SwitchTo(
        Format("{text[language_button]}"),
        id="language",
        state=OptionsSG.language,
    ),
    Cancel(
        Format("{text[back_button]}"),
        id="cancel",
    ),
    state=OptionsSG.main,
    getter=getter,
)
