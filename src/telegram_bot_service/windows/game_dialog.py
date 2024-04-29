from copy import deepcopy
import datetime
from math import ceil
from typing import Any, Dict

from aiogram.types import CallbackQuery

from aiogram_dialog import Data, Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Start,
    Group,
    Row,
    Cancel,
    Next,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const
from aiogram.types import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia


from windows.states import MainMenuSG, PaginationSG, GameDialogSG
from windows.states import not_implemented_yet, ignore
from aiogram_dialog.widgets.kbd import (
    Button,
    ScrollingGroup,
    Select,
    Column,
    CalendarConfig,
)
from aiogram_dialog.widgets.text import Const
import operator
from typing import Any

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format
from datetime import date

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar
from typing import Dict

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Calendar,
    CalendarScope,
    CalendarUserConfig,
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
)
from aiogram_dialog.widgets.text import Const, Format


class CustomCalendar(Calendar):
    # def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
    #     return {
    #         CalendarScope.DAYS: CalendarDaysView(
    #             self._item_callback_data,
    #             self.config,
    #             today_text=Format("***"),
    #             header_text=Format("> {date: %B %Y} <"),
    #         ),
    #         CalendarScope.MONTHS: CalendarMonthView(
    #             self._item_callback_data,
    #             self.config,
    #         ),
    #         CalendarScope.YEARS: CalendarYearsView(
    #             self._item_callback_data,
    #             self.config,
    #         ),
    #     }

    # async def _get_user_config(
    #     self,
    #     data: Dict,
    #     manager: DialogManager,
    # ) -> CalendarUserConfig:
    #     return CalendarUserConfig(
    #         firstweekday=7,
    #     )
    pass


async def on_date_selected(
    callback: CallbackQuery, widget, manager: DialogManager, selected_date: date
):
    await callback.answer(str(selected_date))

    await manager.switch_to(GameDialogSG.main)


async def get_game(dialog_manager: DialogManager, aiogd_context, **kwargs):
    print(
        "get_game",
        aiogd_context.dialog_data,
        aiogd_context.start_data,
        flush=True,
    )

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    return dict(
        id=aiogd_context.dialog_data["game_id"],
        title="Game title",
        description="Game description",
    )


dialog = Dialog(
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        Format("{title} {id}"),
        Row(
            SwitchTo(Const("Info"), id="game_info", state=GameDialogSG.info),
            SwitchTo(Const("Booking"), id="game_booking", state=GameDialogSG.booking),
        ),
        Cancel(Const("⬅️ Back"), id="cancel"),
        state=GameDialogSG.main,
        getter=get_game,
    ),
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        Format("{title} {id}"),
        Format("{description}"),
        SwitchTo(Const("⬅️ Back"), id="to_game_menu", state=GameDialogSG.main),
        state=GameDialogSG.info,
        getter=get_game,
    ),
    Window(
        StaticMedia(
            path="resources/static/menu.jpg",
            type=ContentType.PHOTO,
        ),
        CustomCalendar(
            id="calendar",
            on_click=on_date_selected,
            config=CalendarConfig(min_date=datetime.date.today()),
        ),
        SwitchTo(Const("⬅️ Back"), id="to_game_menu", state=GameDialogSG.main),
        state=GameDialogSG.booking,
        getter=get_game,
    ),
)
