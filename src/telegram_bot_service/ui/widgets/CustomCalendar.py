from datetime import date
from time import mktime
from typing import Dict
from uuid import UUID

from aiogram.types import InlineKeyboardButton

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarDaysView, CalendarScopeView, CalendarMonthView, CalendarYearsView


class CustomCalendarDaysView(CalendarDaysView):
    async def _render_date_button(
        self,
        selected_date: date,
        today: date,
        data: Dict,
        manager: DialogManager,
    ) -> InlineKeyboardButton:
        d_data = manager.current_context().dialog_data

        current_data = {
            "date": selected_date,
            "data": data,
        }
        text = "{date:%d}"

        for booking in d_data["bookings"]:
            booking_date = date.fromisoformat(booking["booking_date"])
            user_id = UUID(booking["user_id"])

            if booking_date == selected_date:
                text = f"🔵{text}" if user_id == d_data["user"].id else f"🔴{text}"

        if selected_date == today:
            text = f"[{text}]"

        text = Format(text)

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
            CalendarScope.MONTHS:
                CalendarMonthView(self._item_callback_data, self.config),
            CalendarScope.YEARS:
                CalendarYearsView(self._item_callback_data, self.config),
        }
