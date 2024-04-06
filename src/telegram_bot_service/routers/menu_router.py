from aiogram import F , Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from keyboards.builders import inline_builder, reply_builder

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == "main_menu")
async def command_start_handler(message: Message | CallbackQuery) -> None:
    keyboard = inline_builder(
        ["All games", "Find with options" ],
        ["list",       "find_with_options"],
        # resize_keyboard=True
    )

    answer = dict(
        text=f"Hello, {hbold(message.from_user.first_name)}!\nThere is some menu",
        reply_markup=keyboard,
    )

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(**answer)
        await message.answer()
    else:
        await message.answer(**answer)
        



