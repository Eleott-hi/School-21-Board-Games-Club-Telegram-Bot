from datetime import date
from time import mktime
from typing import Dict
from uuid import UUID

from aiogram.types import InlineKeyboardButton

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarDaysView, CalendarScopeView


class CustomCalendarDaysView(CalendarDaysView):
    async def _render_date_button(
        self,
        selected_date: date,
        today: date,
        data: Dict,
        manager: DialogManager,
    ):
        dialog_data = manager.current_context().dialog_data

        current_data = {
            "date": selected_date,
            "data": data,
        }
        text = self.date_text

        for booking in dialog_data["bookings"]:
            booking_date = date.fromisoformat(booking["booking_date"])
            user_id = UUID(booking["user_id"])

            if booking_date == selected_date:
                text = Format("🔴 {date:%d}")
                if user_id == dialog_data["user_id"]:
                    text = Format("🔵 {date:%d}")

        if selected_date == today:
            text = self.today_text

        raw_date = int(mktime(selected_date.timetuple()))
        return InlineKeyboardButton(
            text=await text.render_text(
                current_data,
                manager,
            ),
            callback_data=self.callback_generator(str(raw_date)),
        )


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        print(self.config, flush=True)
        return {
            CalendarScope.DAYS: CustomCalendarDaysView(
                self._item_callback_data,
                self.config,
            ),
        }
