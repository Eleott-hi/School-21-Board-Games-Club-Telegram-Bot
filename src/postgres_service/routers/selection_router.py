from uuid import UUID
from datetime import datetime, timedelta, UTC
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends

router = APIRouter(prefix="/db", tags=["test"])


@router.get("/{id}", status_code=200)
async def test(id: int, test_int: int = None):
    return {"message": id + test_int} if test_int else {"message": id}
