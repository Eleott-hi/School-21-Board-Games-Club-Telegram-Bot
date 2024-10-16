import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from schemas.schemas import GamesFiltersWithGenres, GameResponse
from repositories.games_repository import GamesRepository

logger = logging.getLogger(__name__)


class GamesService:
    def __init__(
        self,
        games_repository: GamesRepository = Depends(),
    ):
        self.games_repository = games_repository

    async def get(
        self,
        id: UUID,
    ) -> GameResponse:

        game = await self.games_repository.get(id)
        logger.info(game)
        return GameResponse.model_validate(game)

    async def get_all(
        self,
        filters: GamesFiltersWithGenres,
    ) -> List[GameResponse]:
        res = await self.games_repository.get_all(filters)
        return [GameResponse.model_validate(r) for r in res]
