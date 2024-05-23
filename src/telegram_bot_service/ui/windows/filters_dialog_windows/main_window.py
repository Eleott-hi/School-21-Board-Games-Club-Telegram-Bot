from typing import Any, Dict

from aiogram.types import ContentType
from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia

from ui.states import GameDialogSG, NotFoundSG, PaginationSG, FilterSG

from database.database import MDB
from services.game_service import GameService
from core.Localization import localization

window_text = localization["filters_menu_window"]
common_text = localization["common"]


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

    return {**filters, "genres": ", ".join(filters["genres"])}


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
        Const(window_text["title"]),
        Const(window_text["description"]),
        sep="\n\n",
    ),
    SwitchTo(
        Format(window_text["genre_button"]),
        id="genre",
        state=FilterSG.genre,
    ),
    SwitchTo(
        Format(window_text["age_button"]),
        id="age",
        state=FilterSG.age,
    ),
    SwitchTo(
        Format(window_text["players_number_button"]),
        id="players_num",
        state=FilterSG.players_num,
    ),
    SwitchTo(
        Format(window_text["duration_button"]),
        id="duration",
        state=FilterSG.duration,
    ),
    SwitchTo(
        Format(window_text["complexity_button"]),
        id="complexity",
        state=FilterSG.complexity,
    ),
    SwitchTo(
        Format(window_text["status_button"]),
        id="status",
        state=FilterSG.status,
    ),
    Row(
        Button(Const(window_text["reset_button"]), id="reset", on_click=reset_filters),
        Button(
            Const(window_text["search_button"]),
            id="search",
            on_click=goto,
        ),
    ),
    Cancel(Const(common_text["back_to_main_menu_button"]), id="cancel"),
    state=FilterSG.main,
    parse_mode="HTML",
    getter=getter,
)
