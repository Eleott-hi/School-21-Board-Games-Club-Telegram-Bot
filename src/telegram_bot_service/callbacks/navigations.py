from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.builders import inline_builder
from database.database import games

router = Router()


@router.callback_query(F.data == "list")
async def show_game_list(query: CallbackQuery):
    button_titles = []
    button_callbacks = []

    for game in games:
        button_titles.append(game["gameName"])
        button_callbacks.append("game_info_callback:" + game["gameName"])

    button_titles.append("⬅️ Back")
    button_callbacks.append("main_menu")

    await query.message.edit_text(
        text=f"There is a list of our games",
        reply_markup=inline_builder(button_titles, button_callbacks, sizes=[1]),
    )
    await query.answer()


@router.callback_query(F.data.regexp("^game_info_callback:"))
async def game_info_callbacks(query: CallbackQuery):
    print("Game info callback:", query.data)

    game = query.data.replace("game_info_callback:", "").strip()
    game = list(filter(lambda x: x["gameName"] == game, games))[0]

    await query.message.edit_text(
        text=f'Title: {game["gameName"]}, {game["year"]}\n\n'
        f'Genre: {game["genre"]}\n'
        f'Players {game["minPlayers"]}-{game["maxPlayers"]}\n'
        f'Min age: {game["minAge"]}\n'
        f'Complexity: {game["gameComplexity"]}\n'
        f'Status: {game["status"]}\n'
        f'Description: {game["gameShortDescription"]}\n',
        reply_markup=inline_builder(["⬅️ Back"], ["list"]),
    )

    await query.answer()


@router.callback_query()
async def common_callbacks(query: CallbackQuery):
    print("Empty callback:", query.data)
    await query.answer()

    raise NotImplementedError


# @router.callback_query(F.data == "profile")
# async def show_profile(query: CallbackQuery):
#     text = query.from_user.id
#     await query.message.edit_text(
#         text=f"ID: {text}",
#         reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
#     )
#     await query.answer()


# @router.callback_query(F.data == "banks")
# async def show_profile(query: CallbackQuery):
#     text = "Bank of America"
#     await query.message.edit_text(
#         text=f"ID: {text}",
#         reply_markup=inline_builder(
#             ["⬅️ Back"],
#             ["main_menu"],
#         ),
#     )

#     await query.answer()
