from typing import Any, Dict

from aiogram.types import CallbackQuery, ContentType

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types.message import Message
from aiogram_dialog.manager.manager import ManagerImpl

from services.game_service import GameService
from windows.states import RegistrationSG, ignore
from windows.registration.registration import window as registration_window
from windows.registration.confirmation import window as confirmation_window
from database.database import MDB

from core.Localization import localization

window_text = localization["registration_window"]
common_text = localization["common"]


dialog = Dialog(
    registration_window,
    confirmation_window,
)
