from datetime import date
from typing import List
from uuid import UUID

from fastapi import Depends
from schemas.schemas import BookingFilters, BookingResponse, BookingRequest
from services.auth_service import AuthService


class BookingService:
    def __init__(self, auth_service: AuthService = Depends()):
        self.auth_service = auth_service

    async def get(self, id: UUID) -> BookingResponse:
        return BookingResponse(
            id=id,
            game_id=id,
            user_id=id,
            booking_date=date.today(),
        )

    async def get_all(self, filters: BookingFilters) -> List[BookingResponse]:
        return []

    async def create(self, telegram_id: int, booking: BookingRequest) -> None:
        user = await self.auth_service.get_user_by_telegram_id(telegram_id)

    async def update(self, telegram_id: int, id: UUID, booking: BookingRequest) -> None:
        user = await self.auth_service.get_user_by_telegram_id(telegram_id)

    async def delete(self, telegram_id: int, id: UUID) -> None:
        user = await self.auth_service.get_user_by_telegram_id(telegram_id)
