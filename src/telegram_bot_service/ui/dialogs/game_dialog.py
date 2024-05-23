from aiogram_dialog import Dialog

from ui.windows.game_dialog_windows.main_window import window as main_window
from ui.windows.game_dialog_windows.info_window import window as info_window
from ui.windows.game_dialog_windows.booking_window import window as booking_window
from ui.windows.game_dialog_windows.collection_window import window as collection_window

dialog = Dialog(
    main_window,
    info_window,
    booking_window,
    collection_window,
)
