from uuid import UUID
from datetime import datetime, timedelta, UTC
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends

router = APIRouter(prefix="/db", tags=["test"])


@router.get("/{id}", status_code=200)
async def create_booking(id: int):
    return {"message": id}
