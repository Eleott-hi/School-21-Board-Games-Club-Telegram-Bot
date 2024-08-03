from copy import deepcopy
from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia

from services.auth_service import AuthService
from services.game_service import GameService
from schemas.schemas import User
from core.Localization import Language, localization_manager
from services.collection_service import CollectionService, CollectionType
from ui.utils import telegram_error_handling_decorator
from ui.states import GameDialogSG, not_implemented_yet


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["game_collection_window"]
    common_text: Dict[str, str] = localization["common"]

    game: Dict = data["chosen_game"]
    d = {"type": data["collection"]["type"] if data["collection"] else "-"}

    return dict(
        title=window_text["title"].format_map(game),
        description=window_text["description"].format_map(d),
        add_to_favorite_button=window_text["add_to_favorite_button"].format_map(data),
        remove_from_favorite_button=window_text[
            "remove_from_favorite_button"
        ].format_map(data),
        add_to_black_list_button=window_text["add_to_black_list_button"].format_map(
            data
        ),
        remove_from_black_list_button=window_text[
            "remove_from_black_list_button"
        ].format_map(data),
        back_button=common_text["back_button"].format_map(data),
    )


async def prepare(s_data: Dict, d_data: Dict, user_mongo: Dict):
    if not d_data:
        d_data.update(**deepcopy(s_data))

    if "user" not in d_data:
        user: User = await AuthService().get_user_by_telegram_id(user_mongo["_id"])
        d_data["user"] = user

    if "chosen_game" not in d_data:
        raise ValueError("chosen_game not in d_data")

    collection = await CollectionService().get_collections(
        filters=dict(game_id=d_data["chosen_game"]["id"], user_id=d_data["user"].id)
    )
    d_data["collection"] = collection[0] if collection else None


async def getter(aiogd_context, user_mongo: Dict, **kwargs):
    s_data = aiogd_context.start_data
    d_data = aiogd_context.dialog_data

    await prepare(s_data, d_data, user_mongo)

    not_in_favorites, in_favorites, not_in_black_list, in_black_list = (
        False,
        False,
        False,
        False,
    )
    collection = d_data["collection"]

    if collection is None:
        not_in_favorites, not_in_black_list = True, True
    elif collection["type"] == CollectionType.FAVORITE:
        in_favorites, not_in_black_list = True, True
    else:
        in_black_list, not_in_favorites = True, True

    return dict(
        text=text(d_data, user_mongo["options"]["language"]),
        photo=MediaAttachment(
            ContentType.PHOTO, path=d_data["chosen_game"]["photo_link"]
        ),
        not_in_favorites=not_in_favorites,
        in_favorites=in_favorites,
        not_in_black_list=not_in_black_list,
        in_black_list=in_black_list,
    )


@telegram_error_handling_decorator
async def add_to_favorite(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    telegram_id = callback.from_user.id
    d_data = manager.dialog_data
    collection, game = d_data["collection"], d_data["chosen_game"]

    if collection and collection["type"] == CollectionType.BLACK_LIST:
        await CollectionService().delete_collection(
            telegram_id=telegram_id, collection_id=collection["id"]
        )

    await CollectionService().create_collection(
        telegram_id=telegram_id, game_id=game["id"], type=CollectionType.FAVORITE
    )

    await manager.show()


@telegram_error_handling_decorator
async def remove_from_favorite(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    telegram_id = callback.from_user.id
    d_data = manager.dialog_data
    collection = d_data["collection"]

    if collection and collection["type"] == CollectionType.FAVORITE:
        await CollectionService().delete_collection(
            telegram_id=telegram_id, collection_id=collection["id"]
        )

        await manager.show()


@telegram_error_handling_decorator
async def add_to_black_list(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    telegram_id = callback.from_user.id
    d_data = manager.dialog_data
    collection, game = d_data["collection"], d_data["chosen_game"]

    if collection and collection["type"] == CollectionType.FAVORITE:
        await CollectionService().delete_collection(
            telegram_id=telegram_id, collection_id=collection["id"]
        )

    await CollectionService().create_collection(
        telegram_id=telegram_id, game_id=game["id"], type=CollectionType.BLACK_LIST
    )

    await manager.show()


@telegram_error_handling_decorator
async def remove_from_black_list(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    telegram_id = callback.from_user.id
    d_data = manager.dialog_data
    collection = d_data["collection"]

    if collection and collection["type"] == CollectionType.BLACK_LIST:
        await CollectionService().delete_collection(
            telegram_id=telegram_id, collection_id=collection["id"]
        )

        await manager.show()


window = Window(
    DynamicMedia("photo"),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
    Button(
        Format("{text[add_to_favorite_button]}"),
        id="add_to_favorites",
        on_click=add_to_favorite,
        when="not_in_favorites",
    ),
    Button(
        Format("{text[remove_from_favorite_button]}"),
        id="remove_from_favorite",
        on_click=remove_from_favorite,
        when="in_favorites",
    ),
    Button(
        Format("{text[add_to_black_list_button]}"),
        id="add_to_black_list",
        on_click=add_to_black_list,
        when="not_in_black_list",
    ),
    Button(
        Format("{text[remove_from_black_list_button]}"),
        id="remove_from_black",
        on_click=remove_from_black_list,
        when="in_black_list",
    ),
    SwitchTo(
        Format("{text[back_button]}"),
        id="back",
        state=GameDialogSG.main,
    ),
    state=GameDialogSG.collections,
    getter=getter,
)
