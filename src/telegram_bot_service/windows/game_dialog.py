import datetime
from datetime import date
from copy import deepcopy
from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import Data, Dialog, DialogManager, Window
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
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
)

from services.game_service import GameService
from windows.states import GameDialogSG, not_implemented_yet
from core.Localization import localization

window_text = localization["game_menu_window"]
common_text = localization["common"]


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


async def getter(dialog_manager: DialogManager, aiogd_context, **kwargs):
    print(aiogd_context.start_data, flush=True)
    print(aiogd_context.dialog_data, flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    data = aiogd_context.dialog_data
    game_info: Dict = await GameService.get_game_by_id(data["game_id"])

    return dict(
        photo=MediaAttachment(ContentType.PHOTO, path=game_info["photo_link"]),
        game_info=game_info,
    )


def pritify_game_info(game: Dict):

    return (
        f'Title: {game["title"]}, {game["year"]}\n\n'
        f'Genre: {game["genre"]}\n'
        f'Players {game["minPlayers"]}-{game["maxPlayers"]}\n'
        f'Min age: {game["minAge"]}\n'
        f'Complexity: {game["gameComplexity"]}\n'
        f'Status: {game["status"]}\n'
        f'Description: {game["gameShortDescription"]}\n'
    )


dialog = Dialog(
    Window(
        DynamicMedia("photo"),
        Format("{game_info[title]}"),
        Row(
            SwitchTo(
                Const(window_text["info_button"]),
                id="game_info",
                state=GameDialogSG.info,
            ),
            SwitchTo(
                Const(window_text["booking_button"]),
                id="game_booking",
                state=GameDialogSG.booking,
            ),
        ),
        Row(
            SwitchTo(
                Const(window_text["collection_button"]),
                id="collections",
                state=GameDialogSG.collections,
            ),
        ),
        Cancel(Const(common_text["back_button"]), id="cancel"),
        state=GameDialogSG.main,
        getter=getter,
    ),
    Window(
        DynamicMedia("photo"),
        Multi(
            Format("{game_info[title]}"),
            Format("{game_info[description]}"),
            sep="\n\n",
        ),
        SwitchTo(
            Const(common_text["back_button"]),
            id="to_game_menu",
            state=GameDialogSG.main,
        ),
        state=GameDialogSG.info,
        getter=getter,
    ),
    Window(
        DynamicMedia("photo"),
        CustomCalendar(
            id="calendar",
            on_click=on_date_selected,
            config=CalendarConfig(min_date=datetime.date.today()),
        ),
        SwitchTo(
            Const(common_text["back_button"]),
            id="to_game_menu",
            state=GameDialogSG.main,
        ),
        state=GameDialogSG.booking,
        getter=getter,
    ),
    Window(
        DynamicMedia("photo"),
        Button(
            Const("❤️ Add to favorite"),
            id="add_to_favorites",
            on_click=not_implemented_yet,
        ),
        SwitchTo(
            Const(common_text["back_button"]),
            id="to_game_menu",
            state=GameDialogSG.main,
        ),
        state=GameDialogSG.collections,
        getter=getter,
    ),
)
