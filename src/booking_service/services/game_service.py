import logging
from typing import Dict
from uuid import UUID
from fastapi import HTTPException, status
import httpx

from config.config import GAME_SERVICE_HOST, GAME_SERVICE_PORT, GAME_SERVICE_VERSION
import services.utils as utils

logger = logging.getLogger(__name__)


class GamesService:
    def __init__(self):
        self.base_url = f"http://{GAME_SERVICE_HOST}:{GAME_SERVICE_PORT}/api/v{GAME_SERVICE_VERSION}"

    async def get_game_by_id(self, id: UUID) -> Dict:
        url = f"{self.base_url}/games/{str(id)}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == status.HTTP_200_OK:
                return response.json()

            err = utils.get_fastapi_error(response)
            logger.error(msg=str(err))

            raise err
