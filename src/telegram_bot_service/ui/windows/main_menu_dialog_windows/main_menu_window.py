from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

from core.Localization import Language, localization_manager
from services.game_service import GameService
from ui.states import (
    FilterSG,
    MainMenuSG,
    PaginationSG,
    ProfileSG,
    TitleSearchSG,
    not_implemented_yet,
)


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["main_menu_window"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        all_games_button=window_text["all_games_button"].format_map(data),
        filters_button=window_text["filters_button"].format_map(data),
        title_search_button=window_text["title_search_button"].format_map(data),
        profile_button=window_text["profile_button"].format_map(data),
        help_button=window_text["help_button"].format_map(data),
    )


async def getter(user_mongo: Dict, **kwargs):
    return dict(
        text=text({}, user_mongo["options"]["language"]),
    )


async def goto_pagination(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    games = await GameService().get_games({})
    await manager.start(state=PaginationSG.main, data=dict(games=games))


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
    Button(
        Format("{text[all_games_button]}"),
        id="all_games",
        on_click=goto_pagination,
    ),
    Start(
        Format("{text[filters_button]}"),
        id="filters",
        state=FilterSG.main,
    ),
    Start(
        Format("{text[title_search_button]}"),
        id="title_search",
        state=TitleSearchSG.main,
    ),
    Start(
        Format("{text[profile_button]}"),
        id="profile",
        state=ProfileSG.main,
    ),
    Button(
        Format("{text[help_button]}"),
        id="help",
        on_click=not_implemented_yet,
    ),
    state=MainMenuSG.main,
    getter=getter,
)
