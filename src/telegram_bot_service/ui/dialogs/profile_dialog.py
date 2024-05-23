from aiogram_dialog import Dialog

from ui.windows.profile_dialog_windows.main_window import window as main_window
from ui.windows.profile_dialog_windows.booking_window import window as booking_window
from ui.windows.profile_dialog_windows.collection_window import (
    window as collection_window,
)

dialog = Dialog(
    main_window,
    collection_window,
    booking_window,
)
