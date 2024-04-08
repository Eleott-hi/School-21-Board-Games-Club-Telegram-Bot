from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from keyboards.builders import inline_builder, reply_builder

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "main_menu")
async def command_start_handler(message: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    keyboard = inline_builder(
        ["All games", "Find with options"],
        ["list",      "find_with_options"],
    )

    answer = dict(
        photo=FSInputFile("resources/static/menu.jpg"),
        caption="Menu",
        reply_markup=keyboard,
    )

    if isinstance(message, CallbackQuery):
        await message.message.delete()
        await message.message.answer_photo(**answer)
        await message.answer()
    else:
        await message.delete()
        await message.answer_photo(**answer)
