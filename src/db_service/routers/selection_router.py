# from datetime import datetime, timedelta, UTC
# from typing import List

import json
from uuid import UUID
from typing import Annotated, Optional, List
from fastapi import APIRouter, status, HTTPException, Depends, Query

from db.database import get_session, get_filtered_games, AsyncSession, select
from db.models import BoardGame, Filters


router = APIRouter(prefix="/db", tags=["test"])


@router.get("/id", status_code=200)
async def get_testing_query(*,
                            name: Annotated[str, Query()], 
                            session: AsyncSession = Depends(get_session)
):
    stmt = select(BoardGame).where(BoardGame.gameName == name)
    result = await session.exec(stmt)
    result_data = [obj.id for obj in result.all()]

    return {"game id" : result_data} if result_data else None


@router.get("/find", status_code=200, response_model=List[BoardGame])
async def get_filtered(*,
                        json_filters: Optional[str] = Query(None, example=json.dumps({
                            "age": 18,
                            "status": "available",
                            "players_num": 4,
                            "duration": 80,
                            "complexity": "hard",
                            "genres": ["strategy", "family", "adventure"],
                            "offset": 0,
                            "limit": 1000
                        })),
                        session: AsyncSession = Depends(get_session)  # Assuming you have session setup
):
    
    try:
        filters = Filters.model_validate(json.loads(json_filters) if json_filters else {})
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    result_data = await get_filtered_games(filters, session)


    return [BoardGame.model_validate(game) for game in result_data]