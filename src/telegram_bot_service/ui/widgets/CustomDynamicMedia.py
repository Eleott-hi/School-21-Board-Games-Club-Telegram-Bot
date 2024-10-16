from operator import itemgetter
from typing import Callable, Optional, Union

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.media import DynamicMedia


class CustomDynamicMedia(DynamicMedia):
    async def _render_media(
        self,
        data: dict,
        manager: DialogManager,
    ) -> Optional[MediaAttachment]:
        media = None 
        
        try:
            media: Optional[MediaAttachment] = self.selector(data)
        except Exception as e:
            print(e)

        return media
