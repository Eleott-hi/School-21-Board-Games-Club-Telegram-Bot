from datetime import date
import logging
from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Header, status, Depends, Query
from schemas.schemas import (
    GameResponse,
    GamesFiltersWithGenres,
    GamesFiltersWithoutGenres,
    Genre,
)
from services.game_service import GamesService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/games",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
async def get_all_games(
    genres: List[Genre] = Query(None),
    filters: GamesFiltersWithoutGenres = Depends(),
    game_service: GamesService = Depends(),
):
    filters = GamesFiltersWithGenres(**filters.model_dump(), genres=genres)
    res = await game_service.get_all(filters)
    return res


@router.get(
    "/games/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
    },
)
async def get_game(
    id: UUID,
    game_service: GamesService = Depends(),
) -> GameResponse:
    res = await game_service.get(id)
    return res
