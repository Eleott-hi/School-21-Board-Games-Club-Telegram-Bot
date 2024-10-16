from aiogram_dialog import Dialog

from ui.windows.profile_collection_dialog_windows.main_window import (
    window as main_window,
)
from ui.windows.profile_collection_dialog_windows.pagination_window import (
    window as pagination_window,
)

dialog = Dialog(
    main_window,
    pagination_window,
)
