from typing import Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types.message import Message
from aiogram_dialog.manager.manager import ManagerImpl

from services.game_service import GameService
from ui.states import GameDialogSG, TelegramErrorSG, PaginationSG, TitleSearchSG
from database.database import MDB

from core.Localization import localization_manager


def text(data: Dict, language: str) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text = localization["title_search_menu_window"]
    common_text = localization["common"]

    return dict(
        title=window_text["title"].format_map(data),
        description=window_text["description"].format_map(data),
        current_input=window_text["current_input"].format_map(data),
        search_button=window_text["search_button"].format_map(data),
        reset_button=window_text["reset_button"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
        back_to_main_menu_button=common_text["back_to_main_menu_button"].format_map(
            data,
        ),
    )


async def getter(
    aiogd_context,
    db: MDB,
    user_mongo: Dict,
    **kwargs,
):
    print("aiogd_context", aiogd_context, flush=True)
    print("user_mongo", user_mongo, flush=True)

    if not aiogd_context.widget_data:
        aiogd_context.widget_data = dict(
            location="Title",
            input="",
        )

    data = aiogd_context.widget_data

    return dict(
        text=text(data, user_mongo["options"]["language"]),
    )


async def goto(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    data = manager.current_context().widget_data
    options = manager.middleware_data["user_mongo"]["options"]

    filters = dict(offset=0, limit=options["pagination_limit"], title=data["input"])

    games = await GameService().get_games(filters)

    if games["total"] == 0:
        await manager.start(TelegramErrorSG.main)

    elif games["total"] == 1:
        game_id = games["games"][0]["id"]
        await manager.start(GameDialogSG.main, data=dict(game_id=game_id))

    else:
        await manager.start(PaginationSG.main, data=filters)


async def reset_filters(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    manager.current_context().widget_data = dict(
        location="Title",
        input="",
    )

    await manager.show()


async def user_input_text(
    message: Message,
    b: MessageInput,
    manager: ManagerImpl,
):
    print(message.text, flush=True)

    manager.current_context().widget_data["input"] = message.text


window = Window(
    StaticMedia(
        path="resources/static/filter.jpg",
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("{text[title]}"),
        Multi(
            Format("{text[description]}"),
            Format("{text[current_input]}"),
        ),
        sep="\n\n",
    ),
    MessageInput(
        user_input_text,
        content_types=ContentType.TEXT,
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
    state=TitleSearchSG.main,
    parse_mode="HTML",
    getter=getter,
)
