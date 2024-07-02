from typing import List, Dict
from config import GAMES_SERVICE_HOST, GAMES_SERVICE_PORT, GAMES_SERVICE_VERSION
import httpx
from fastapi import status
from urllib.parse import urlencode

from core.Exceptions import TelegramException, process_fastapi_error



class GameService:
    def __init__(self):
        self.base_url = f"http://{GAMES_SERVICE_HOST}:{GAMES_SERVICE_PORT}/api/v{GAMES_SERVICE_VERSION}"

    async def get_games(self, filters: Dict):
        url = f"{self.base_url}/games?{urlencode({k:v for k,v in filters.items() if v is not None and v != []})}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != status.HTTP_200_OK:
                process_fastapi_error(response)
            
            res = response.json()
            return dict(
                    games=self.__clamp_games_with_offset_and_limit(filters, res),
                    total=len(res),
                )

        

    async def get_game_by_id(self, id: str) -> Dict:
        url = f"{self.base_url}/games/{id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == status.HTTP_200_OK:
                res = response.json()
                return res

        raise TelegramException("Game not found")

    def __clamp_games_with_offset_and_limit(self, filters, games):
        """
        TODO remove this logic here, unnessesary multiple time calling
        """
        print("__clamp_games_with_offset_and_limit: FIX ME")
        offset = filters.get("offset", 0)
        limit = filters.get("limit", 3)
        from_ = offset
        to_ = from_ + limit
        return games[from_:to_]
