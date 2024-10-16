import datetime
from datetime import date
from copy import deepcopy
from typing import Any, Dict
from uuid import UUID

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import (
    SwitchTo,
    CalendarConfig,
)
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.media import DynamicMedia

from schemas.schemas import User
from services.game_service import GameService
from services.booking_service import BookingService
from core.Localization import Language, localization_manager
from core.Exceptions import TelegramException
from services.auth_service import AuthService
from ui.states import GameDialogSG, TelegramErrorSG
from ui.widgets.CustomCalendar import CustomCalendar
import ui.utils


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    window_text: Dict[str, str] = localization["game_booking_window"]
    common_text: Dict[str, str] = localization["common"]

    game = data["chosen_game"]

    return dict(
        title=window_text["title"].format_map(game),
        description=window_text["description"].format_map(data),
        back_button=common_text["back_button"].format_map(data),
        back_to_main_menu_button=common_text["back_to_main_menu_button"].format_map(
            data
        ),
    )


async def getter(
    aiogd_context: Context,
    user_mongo: Dict,
    **kwargs,
):
    s_data = aiogd_context.start_data
    d_data = aiogd_context.dialog_data

    if not d_data:
        d_data.update(**deepcopy(s_data))

    if "user" not in d_data:
        user: User = await AuthService().get_user_by_telegram_id(user_mongo["_id"])
        d_data["user"] = user

    if "chosen_game" not in d_data:
        raise ValueError("chosen_game not in d_data")

    filters = dict(game_id=d_data["chosen_game"]["id"])
    bookings: Dict = await BookingService().get_bookings(filters=filters)
    d_data["bookings"] = bookings

    print(d_data, flush=True)

    return dict(
        text=text(d_data, user_mongo["options"]["language"]),
        photo=MediaAttachment(
            ContentType.PHOTO, url=d_data["chosen_game"]["photo_link"]
        ),
    )


@ui.utils.telegram_error_handling_decorator
async def on_date_selected(
    callback: CallbackQuery,
    widget,
    manager: DialogManager,
    selected_date: date,
):
    d_data = manager.current_context().dialog_data

    bookings = d_data["bookings"]
    print(bookings, flush=True)

    already_booked_for_this_user_and_this_date = [
        b
        for b in bookings
        if UUID(b["user_id"]) == d_data["user"].id
        and date.fromisoformat(b["booking_date"]) == selected_date
    ]

    print(
        "already_booked_for_this_user_and_this_date",
        already_booked_for_this_user_and_this_date,
        flush=True,
    )

    if already_booked_for_this_user_and_this_date:
        booking = already_booked_for_this_user_and_this_date[0]
        await BookingService().remove_booking(
            telegram_id=callback.from_user.id,
            booking_id=booking["id"],
        )
        await callback.answer("You've canceled your booking on " + str(selected_date))

    else:
        res = await BookingService().create_booking(
            telegram_id=callback.from_user.id,
            game_id=d_data["chosen_game"]["id"],
            booking_date=selected_date,
        )
        await callback.answer("You've booked this game on " + str(selected_date))


window = Window(
    DynamicMedia("photo"),
    Multi(
        Format("{text[title]}"),
        Format("{text[description]}"),
        sep="\n\n",
    ),
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
    ui.utils.default_back_to_main_menu_button(),
    state=GameDialogSG.booking,
    getter=getter,
)
