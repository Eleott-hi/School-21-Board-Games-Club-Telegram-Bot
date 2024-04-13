import logging
import asyncio
import sys
from datetime import datetime

from aiogram3_calendar import SimpleCalendar, DialogCalendar
from aiogram3_calendar.calendar_types import (
    SimpleCalendarCallback,
    DialogCalendarCallback,
)


from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.utils.markdown import hbold

router = Router()


@router.message(F.text.lower() == "navigation calendar")
async def nav_cal_handler(message: Message):
    import calendar

    year: int = datetime.now().year + 1
    month: int = datetime.now().month
    month_calendar = calendar.monthcalendar(year, month)

    print(month_calendar, flush=True)

    await message.answer(
        "Please select a date: ", reply_markup=await SimpleCalendar().start_calendar()
    )


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(
    callback_query: CallbackQuery, callback_data: CallbackData
):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'You selected {date:"%d/%m/%Y"}')
