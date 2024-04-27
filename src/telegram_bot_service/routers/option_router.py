# from aiogram import F, Router
# from aiogram.types import ReplyKeyboardRemove, CallbackQuery, Message
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from keyboards.builders import reply_builder

# router = Router()


# # Алгоритм поиска игр
# # 1) число игроков [any, input]
# # 2) продолжительность (в минутах) [any, 15, 30, 45, 60, 90, 120, 180, 240]
# # 3) сложность [any, 1,2,3,4,5] (или вообще не делать этот фильтр?)
# # 4) возрастная категория (возраст младшего игрока) [any, imput])
# # 5) жанр [any, 'Азартные', 'Война', 'Карты', 'Классика', 'Компанейские', 'Логические', 'Приключения','Экономика'];
# # 6) availability [any, available_only, not_available_only]


# class GameFilterForm(StatesGroup):
#     START = State()
#     PLAYERS_NUM_SELECTED = State()
#     DURATION_SELECTED = State()
#     COMPLEXITY_SELECTED = State()
#     AGE_SELECTED = State()
#     GENRE_SELECTED = State()


# @router.callback_query(F.data == "find_with_options")
# async def start_filtered_game_search(query: CallbackQuery, state: FSMContext) -> None:
#     message = query.message
#     await state.set_state(GameFilterForm.START)

#     keyboard = reply_builder(
#         ["Any"],
#         sizes=[1],
#         resize_keyboard=True,
#     )

#     await message.answer(
#         text="Number of players:",
#         reply_markup=keyboard,
#     )

#     await query.answer()


# @router.message(GameFilterForm.START)
# async def select_players_number(message: Message, state: FSMContext) -> None:
#     input = message.text

#     await state.update_data(players_num=input)
#     await state.set_state(GameFilterForm.PLAYERS_NUM_SELECTED)

#     keyboard = reply_builder(
#         ["Any", "15", "30", "45", "60", "90", "120", "180", "240"],
#         sizes=[1],
#         resize_keyboard=True,
#     )

#     await message.answer(
#         text="Duration (min):",
#         reply_markup=keyboard,
#     )


# @router.message(GameFilterForm.PLAYERS_NUM_SELECTED)
# async def select_duration(message: Message, state: FSMContext) -> None:
#     input = message.text

#     await state.update_data(duration=input)
#     await state.set_state(GameFilterForm.DURATION_SELECTED)

#     keyboard = reply_builder(
#         ["Any", "1", "2", "3", "4", "5"],
#         sizes=[1],
#         resize_keyboard=True,
#     )

#     await message.answer(
#         text="Complexity:",
#         reply_markup=keyboard,
#     )


# @router.message(GameFilterForm.DURATION_SELECTED)
# async def select_complexity(message: Message, state: FSMContext) -> None:
#     input = message.text

#     await state.update_data(complexity=input)
#     await state.set_state(GameFilterForm.COMPLEXITY_SELECTED)

#     keyboard = reply_builder(
#         ["Any"],
#         sizes=[1],
#         resize_keyboard=True,
#     )

#     await message.answer(
#         text="Younger player's age",
#         reply_markup=keyboard,
#     )


# @router.message(GameFilterForm.COMPLEXITY_SELECTED)
# async def select_age(message: Message, state: FSMContext) -> None:
#     input = message.text

#     await state.update_data(age=input)
#     await state.set_state(GameFilterForm.AGE_SELECTED)

#     keyboard = reply_builder(
#         [
#             "Any",
#             "Азартные",
#             "Война",
#             "Карты",
#             "Классика",
#             "Компанейские",
#             "Логические",
#             "Приключения",
#             "Экономика",
#         ],
#         sizes=[1],
#         resize_keyboard=True,
#     )

#     await message.answer(
#         text="Genre",
#         reply_markup=keyboard,
#     )


# @router.message(GameFilterForm.AGE_SELECTED)
# async def select_game(message: Message, state: FSMContext) -> None:
#     input = message.text

#     await state.update_data(game=input)
#     await state.set_state(GameFilterForm.GENRE_SELECTED)

#     keyboard = reply_builder(
#         ["Any", "available_only", "not_available_only"],
#         sizes=[1],
#         resize_keyboard=True,
#     )

#     await message.answer(
#         text="Availability:",
#         reply_markup=keyboard,
#     )


# @router.message(GameFilterForm.GENRE_SELECTED)
# async def select_availability(message: Message, state: FSMContext) -> None:
#     input = message.text
#     filters = await state.update_data(availability=input)
#     await state.clear()

#     print(filters)
#     await message.answer(f"Filters: {filters}", reply_markup=ReplyKeyboardRemove())


# # @router.message(GameFilterForm, F.text == "cancel")
# # async def cancel_handler(message: Message, state: FSMContext) -> None:
# #     """
# #     Allow user to cancel any action
# #     """
# #     print("HERE")

# #     # current_state = await state.get_state()
# #     # if current_state is None:
# #     #     return

# #     # logging.info("Cancelling state %r", current_state)
# #     # await state.clear()
# #     # await message.answer(
# #     #     "Cancelled.",
# #     #     reply_markup=ReplyKeyboardRemove(),
# #     # )
