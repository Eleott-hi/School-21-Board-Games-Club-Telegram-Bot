from uuid import UUID
from typing import Annotated
from datetime import datetime, timedelta, UTC
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Query, Path

from db.database import get_session, AsyncSession, select

from db.models import BoardGame

router = APIRouter(prefix="/db", tags=["test"])

@router.get("/{name}", status_code=200)
async def get_testing_query(name: Annotated[str, Path()], 
                            session: AsyncSession = Depends(get_session)):
    stmt = select(BoardGame).where(BoardGame.gameName == name)
    result = await session.exec(stmt)
    result_data = [obj.id for obj in result.all()]

    return {"game id" : result_data} if result_data else None

# in progress..
@router.post("/{name}", status_code=200)
async def insert_new_game(game: Annotated[BoardGame, Query()]):
    async with get_session() as session:
        session.add(game)
        await session.commit()