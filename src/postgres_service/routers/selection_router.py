from uuid import UUID
from typing import Annotated
from datetime import datetime, timedelta, UTC
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Query, Path

router = APIRouter(prefix="/db", tags=["test"])


@router.get("/{id}", status_code=200)
async def test(id: Annotated[int, Path(title = "test id")], test_int: Annotated[int, Query()] = None):
    return {"message": id + test_int} if test_int else {"message": id}


