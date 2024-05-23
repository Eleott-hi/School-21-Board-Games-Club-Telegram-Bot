import datetime
from datetime import date
from copy import deepcopy
from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Row,
    Cancel,
    SwitchTo,
    Calendar,
    CalendarScope,
    CalendarUserConfig,
    CalendarConfig,
)
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
)

from services.game_service import GameService
from core.Localization import Language, localization_manager
from ui.states import GameDialogSG


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


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        back_button=common_text["back_button"].format_map(data),
    )


async def on_date_selected(
    callback: CallbackQuery,
    widget,
    manager: DialogManager,
    selected_date: date,
):
    await callback.answer(str(selected_date))
    # await manager.switch_to(GameDialogSG.main)


async def getter(
    aiogd_context,
    user_mongo: Dict,
    **kwargs,
):
    print(aiogd_context.start_data, flush=True)
    print(aiogd_context.dialog_data, flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    data = aiogd_context.dialog_data
    game: Dict = await GameService.get_game_by_id(data["game_id"])

    return dict(
        text=text({}, user_mongo["options"]["language"]),
        photo=MediaAttachment(ContentType.PHOTO, path=game["photo_link"]),
        game=game,
    )


window = Window(
    DynamicMedia("photo"),
    CustomCalendar(
        id="calendar",
        on_click=on_date_selected,
        config=CalendarConfig(min_date=datetime.date.today()),
    ),
    SwitchTo(
        Format("{text[back_button]}"),
        id="back",
        state=GameDialogSG.main,
    ),
    state=GameDialogSG.booking,
    getter=getter,
)
