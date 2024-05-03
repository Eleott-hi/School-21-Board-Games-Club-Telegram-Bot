# from datetime import datetime, timedelta, UTC
# from typing import List

from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends, Query, Path, Body

from db.database import get_session, get_filtered_games, AsyncSession, select
from db.models import BoardGame
from routers.schemas import (
    Filters
)



router = APIRouter(prefix="/db", tags=["test"])


@router.get("/id", status_code=200)
async def get_testing_query(name: Annotated[str, Query()], 
                            session: AsyncSession = Depends(get_session)):
    stmt = select(BoardGame).where(BoardGame.gameName == name)
    result = await session.exec(stmt)
    result_data = [obj.id for obj in result.all()]

    return {"game id" : result_data} if result_data else None


@router.get("/find", status_code=200)
async def get_filtered(game: Filters = Body()):
    result_data = await get_filtered_games(game)
    print(result_data)
    return {result_data}