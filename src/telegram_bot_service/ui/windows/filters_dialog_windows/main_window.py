from typing import Any, Dict

from aiogram.types import ContentType
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

from ui.states import GameDialogSG, NotFoundSG, PaginationSG, FilterSG

from database.database import MDB
from services.game_service import GameService
from core.Localization import localization_manager, Language


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text = localization["filters_menu_window"]
    common_text = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        age_button=window_text["age_button"].format_map(data),
        genre_button=window_text["genre_button"].format_map(data),
        players_number_button=window_text["players_number_button"].format_map(data),
        duration_button=window_text["duration_button"].format_map(data),
        complexity_button=window_text["complexity_button"].format_map(data),
        status_button=window_text["status_button"].format_map(data),
        reset_button=window_text["reset_button"].format_map(data),
        search_button=window_text["search_button"].format_map(data),
        back_to_main_menu_button=common_text["back_to_main_menu_button"].format_map(
            data
        ),
    )


def get_filters_from_user_mongo(user_mongo: Dict) -> Dict[str, Any]:
    filters: Dict[str, Any] = user_mongo["optional_filters"]
    filters = {key: value if value else "Any" for key, value in filters.items()}

    if filters["genres"] == "Any":
        filters["genres"] = [filters["genres"]]

    return filters


async def getter(aiogd_context, db: MDB, user_mongo: Dict, **kwargs):
    print("getter", flush=True)
    print("aiogd_context", aiogd_context, flush=True)
    print("user_mongo", user_mongo, flush=True)

    filters: Dict[str, Any] = get_filters_from_user_mongo(user_mongo)

    if not aiogd_context.widget_data:
        aiogd_context.widget_data = filters

    return dict(
        text=text(
            {**filters, "genres": ", ".join(filters["genres"])},
            user_mongo["options"]["language"],
        )
    )


async def goto(callback: CallbackQuery, button: Button, manager: DialogManager):
    user = manager.middleware_data["user_mongo"]
    options = user["options"]
    filters = user["optional_filters"]
    filters = dict(offset=0, limit=options["pagination_limit"], **filters)

    games = await GameService.get_games(filters)

    if games["total"] == 0:
        await manager.start(NotFoundSG.main)

    elif games["total"] == 1:
        game_id = games["games"][0]["id"]
        await manager.start(GameDialogSG.main, data=dict(game_id=game_id))

    else:
        await manager.start(PaginationSG.main, data=filters)


async def reset_filters(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    user = manager.middleware_data["user_mongo"]
    filters = user["optional_filters"]
    db = manager.middleware_data["db"]

    for key in filters:
        filters[key] = None

    await db.users.replace_one({"_id": user["_id"]}, user)
    manager.current_context().widget_data = {}
    await manager.show()


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
    SwitchTo(
        Format("{text[genre_button]}"),
        id="genre",
        state=FilterSG.genre,
    ),
    SwitchTo(
        Format("{text[age_button]}"),
        id="age",
        state=FilterSG.age,
    ),
    SwitchTo(
        Format("{text[players_number_button]}"),
        id="players_num",
        state=FilterSG.players_num,
    ),
    SwitchTo(
        Format("{text[duration_button]}"),
        id="duration",
        state=FilterSG.duration,
    ),
    SwitchTo(
        Format("{text[complexity_button]}"),
        id="complexity",
        state=FilterSG.complexity,
    ),
    SwitchTo(
        Format("{text[status_button]}"),
        id="status",
        state=FilterSG.status,
    ),
    Row(
        Button(
            Format("{text[reset_button]}"),
            id="reset",
            on_click=reset_filters,
        ),
        Button(
            Format("{text[search_button]}"),
            id="search",
            on_click=goto,
        ),
    ),
    Cancel(
        Format("{text[back_to_main_menu_button]}"),
        id="cancel",
    ),
    state=FilterSG.main,
    parse_mode="HTML",
    getter=getter,
)
