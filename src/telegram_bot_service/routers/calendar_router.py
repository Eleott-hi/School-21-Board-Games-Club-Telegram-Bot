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

from callbacks.callback_data import Transfer, Screen
from services.utils import create_or_edit_media
from keyboards.builders import inline_builder

router = Router()


@router.callback_query(Transfer.filter(F.to_ == Screen.CALENDAR))
async def nav_cal_handler(query: CallbackQuery):
    message = query.message
    await create_or_edit_media(
        message=message,
        photo="resources/static/booking.jpg",
        caption="Please select a date: ",
        reply_markup=await SimpleCalendar().start_calendar(),
        edit=True,
    )

    await query.answer()


@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(query: CallbackQuery, callback_data: CallbackData):
    message = query.message

    print(callback_data, flush=True)

    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(query, callback_data)

    if selected:
        await create_or_edit_media(
            message=message,
            photo="resources/static/booking.jpg",
            caption="You booked on: " + date.strftime("%d.%m.%Y"),
            reply_markup=inline_builder(
                text=["⬅️ Back to Main Menu"],
                callback_data=[Transfer(to_=Screen.MAIN_MENU).pack()],
            ),
            edit=True,
        )

    await query.answer()
