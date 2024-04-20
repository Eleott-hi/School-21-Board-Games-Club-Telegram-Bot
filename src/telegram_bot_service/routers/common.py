from typing import Dict, Optional
from keyboards.builders import inline_builder
from services.utils import create_or_edit_media
from services.game_service import pritify_game_info
from callbacks.callback_data import (
    Screen,
    Transfer,
)
from keyboards.keyboards import (
    filter_search_keyboard,
    main_menu_keyboard,
    game_menu_keyboard,
    games_list_keyboard,
    number_of_players_kb,
    duartion_kb,
    complexity_kb,
    age_kb,
    genre_kb,
    status_kb,
)


async def display_main_menu(message, edit):
    await create_or_edit_media(
        message=message,
        photo="resources/static/menu.jpg",
        caption="Menu",
        reply_markup=main_menu_keyboard(),
        edit=edit,
    )


async def display_game_menu(message, game, from_: Optional[Screen], edit: bool):
    await create_or_edit_media(
        message=message,
        photo=game["photo_link"],
        caption=f"{game['title']}, {game['year']}",
        reply_markup=game_menu_keyboard(game_id=game["id"], from_=from_),
        edit=edit,
    )


async def display_game_info(message, game, from_: Optional[Screen], edit: bool):
    await create_or_edit_media(
        message,
        photo=game["photo_link"],
        caption=pritify_game_info(game),
        reply_markup=inline_builder(
            ["⬅️ Back"],
            [Transfer(to_=Screen.GAME_MENU, from_=from_, meta_=game["id"]).pack()],
        ),
        edit=edit,
    )


async def display_game_not_found(
    message,
    edit,
    caption="Nothing was found",
):
    await create_or_edit_media(
        message,
        photo="resources/static/not_found.jpg",
        caption=caption,
        reply_markup=inline_builder(
            ["⬅️ Back to Main Menu"], [Transfer(to_=Screen.MAIN_MENU).pack()]
        ),
        edit=edit,
    )


async def display_game_list(message, data, edit):
    await create_or_edit_media(
        message,
        photo="resources/static/menu.jpg",
        caption=f"Found {data['total']} games",
        reply_markup=games_list_keyboard(data),
        edit=edit,
    )


async def display_filtered_search(message, filters: Dict, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Enter game title",
        reply_markup=filter_search_keyboard(filters),
        edit=edit,
    )


async def display_players_num_filter(message, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Choose number fo players",
        reply_markup=number_of_players_kb(),
        edit=edit,
    )


async def display_duration_filter(message, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Choose desired duration",
        reply_markup=duartion_kb(),
        edit=edit,
    )


async def display_complexity_filter(message, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Choose desired complexity",
        reply_markup=complexity_kb(),
        edit=edit,
    )


async def display_age_filter(message, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Choose desired age",
        reply_markup=age_kb(),
        edit=edit,
    )


async def display_genre_filter(message, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Choose desired genre",
        reply_markup=genre_kb(),
        edit=edit,
    )


async def display_status_filter(message, edit: bool):
    await create_or_edit_media(
        message,
        photo="resources/static/filter.jpg",
        caption="Choose desired status",
        reply_markup=status_kb(),
        edit=edit,
    )
