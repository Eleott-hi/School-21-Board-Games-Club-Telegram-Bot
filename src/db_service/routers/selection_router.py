# from datetime import datetime, timedelta, UTC
# from typing import List

from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends, Query, Path, Body

from db.database import get_session, AsyncSession, select
from db.models import BoardGame
from routers.schemas import (
    TestGameWateredDown,
    TestState
)

router = APIRouter(prefix="/db", tags=["test"])


@router.get("/id", status_code=200)
async def get_testing_query(name: Annotated[str, Query()], 
                            session: AsyncSession = Depends(get_session)):
    stmt = select(BoardGame).where(BoardGame.gameName == name)
    result = await session.exec(stmt)
    result_data = [obj.id for obj in result.all()]

    return {"game id" : result_data} if result_data else None


@router.post("/change_state", status_code=200)
async def change_state(data: TestState = Body(),
                       session: AsyncSession = Depends(get_session)):
    stmt = select(BoardGame).where(BoardGame.gameName == data.gameName)
    result = await session.exec(stmt)
    result_data = result.all()

    if result_data:
        for game in result_data:
            game.status = data.status
            await session.commit()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Game with name '{data.gameName}' not found")
    
    
@router.post("/insertgame", status_code=201)
async def insert_new_game(game: TestGameWateredDown = Body(),
                          session: AsyncSession = Depends(get_session)):
    game = BoardGame(**game.dict()) # The `dict` method is deprecated; use `model_dump` instead.

    session.add(game)
    await session.commit()
    return{"status": "success"}