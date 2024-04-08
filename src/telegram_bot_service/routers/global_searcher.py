
from aiogram import Router
from aiogram.types import Message
from keyboards.builders import inline_builder
from services.game_service import pritify_game_info, form_game_buttons, get_games_by_str_in_title
router = Router()

@router.message()
async def find_games_according_to_input(message: Message):
    title: str = message.text
    message = await message.answer(f"Searching for games on request: {message.text}")

    games = await get_games_by_str_in_title(title)

    if not games:
        await message.edit_text(f"No games found on request: {title}")

    elif len(games) == 1:
        await message.edit_text(
            text=pritify_game_info(games[0]),
            reply_markup=inline_builder(["⬅️ Back"], ["main_menu"]),
        )
    else:
        buttons, callbacks = form_game_buttons(games)
        await message.edit_text(
            text=f"Found {len(games)} games on request: {title}",
            reply_markup=inline_builder(
                buttons + ["⬅️ Back"],
                callbacks + ["main_menu"],
                sizes=[1],
            ),
        )
