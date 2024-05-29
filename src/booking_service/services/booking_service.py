from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends
from schemas.schemas import BookingFilters, BookingResponse, BookingRequest, User
from services.auth_service import AuthService
from repositories.booking_repository import BookingRepository

logger = logging.getLogger(__name__)

class BookingService:
    def __init__(
        self,
        auth_service: AuthService = Depends(),
        booking_repository: BookingRepository = Depends(),
    ):
        self.auth_service = auth_service
        self.booking_repository = booking_repository

    async def get(self, id: UUID) -> BookingResponse:
        bookingORM = await self.booking_repository.get(id)
        logger.info(bookingORM.id)
        return BookingResponse(
            id=bookingORM.id,
            game_id=bookingORM.game_id,
            user_id=bookingORM.user_id,
            booking_date=bookingORM.booking_date,
        )

    async def get_all(self, filters: BookingFilters) -> List[BookingResponse]:
        return []

    async def create(self, user: User, booking: BookingRequest) -> None:
        pass

    async def update(self, user: User, id: UUID, booking: BookingRequest) -> None:
        pass

    async def delete(self, user: User, id: UUID) -> None:
        pass
