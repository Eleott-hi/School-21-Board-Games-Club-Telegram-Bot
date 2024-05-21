from aiogram_dialog import Dialog
from ui.windows.registration_dialog_windows.registration import (
    window as registration_window,
)
from ui.windows.registration_dialog_windows.confirmation import (
    window as confirmation_window,
)


dialog = Dialog(
    registration_window,
    confirmation_window,
)
