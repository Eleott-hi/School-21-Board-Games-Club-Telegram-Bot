import datetime
from datetime import date
from copy import deepcopy
from typing import Any, Dict

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
from ui.states import GameDialogSG
from ui.widgets.CustomCalendar import CustomCalendar


def text(data: Dict[str, Any], language: str | Language) -> Dict[str, str]:
    localization = localization_manager[language]
    common_text: Dict[str, str] = localization["common"]

    return dict(
        back_button=common_text["back_button"].format_map(data),
    )


async def getter(
    aiogd_context: Context,
    user_mongo: Dict,
    **kwargs,
):
    print(aiogd_context.start_data, flush=True)
    print(aiogd_context.dialog_data, flush=True)
    print(aiogd_context, type(aiogd_context), flush=True)

    if not aiogd_context.dialog_data:
        aiogd_context.dialog_data = deepcopy(aiogd_context.start_data)

    data = aiogd_context.dialog_data
    game: Dict = await GameService().get_game_by_id(data["game_id"])
    bookings: Dict = await BookingService().get_bookings()
    user: User = await AuthService().get_user_by_telegram_id(user_mongo["_id"])
    data["bookings"] = bookings
    data["user_id"] = user.id

    print(data, flush=True)

    return dict(
        text=text({}, user_mongo["options"]["language"]),
        photo=MediaAttachment(ContentType.PHOTO, path=game["photo_link"]),
        # game=game,
    )


async def on_date_selected(
    callback: CallbackQuery,
    widget,
    manager: DialogManager,
    selected_date: date,
):
    data = manager.current_context().dialog_data
    # print(manager.current_context(), flush=True)
    # print(widget, flush=True)

    try:
        res = await BookingService().create_booking(
            telegram_id=callback.from_user.id,
            game_id=data["game_id"],
            booking_date=selected_date,
        )
    except TelegramException as e:
        print(e.exception_type, flush=True)
        pass
    else:
        await callback.answer(str(selected_date))
    # await manager.switch_to(GameDialogSG.main)


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
