from aiogram_dialog import Dialog

from ui.windows.filters_dialog_windows.main_window import window as main_window
from ui.windows.filters_dialog_windows.age_window import window as age_window
from ui.windows.filters_dialog_windows.genre_window import window as genre_window
from ui.windows.filters_dialog_windows.status_window import window as status_window
from ui.windows.filters_dialog_windows.players_window import window as players_window
from ui.windows.filters_dialog_windows.duration_window import window as duration_window
from ui.windows.filters_dialog_windows.complexity_window import (
    window as complexity_window,
)


dialog = Dialog(
    main_window,
    genre_window,
    age_window,
    players_window,
    duration_window,
    complexity_window,
    status_window,
)
