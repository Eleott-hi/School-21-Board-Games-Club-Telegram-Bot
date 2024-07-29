import logging
from typing import Dict
from uuid import UUID

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class GamesService:
    def __init__(self):
        pass

    async def get_game_by_id(cls, id: UUID) -> Dict:
        try:
            res = {"id": id}
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return res
