from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
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

    async def get(
        self,
        id: UUID,
    ) -> BookingResponse:

        booking = await self.booking_repository.get(id)
        return BookingResponse.model_validate(booking)

    async def get_all(
        self,
        filters: BookingFilters,
    ) -> List[BookingResponse]:
        res = await self.booking_repository.get_all(filters)
        print(res, flush=True)
        return [BookingResponse.model_validate(r) for r in res]

    async def create(
        self,
        user: User,
        booking: BookingRequest,
    ) -> BookingResponse:

        new_booking = await self.booking_repository.create(user.id, booking)
        return BookingResponse.model_validate(new_booking)

    async def update(
        self,
        user: User,
        id: UUID,
        booking: BookingRequest,
    ) -> None:
        db_booking = await self.get(id)
        if db_booking.user_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        await self.booking_repository.update(user.id, id, booking)
        return

    async def delete(
        self,
        user: User,
        id: UUID,
    ) -> None:
        db_booking = await self.get(id)
        if db_booking.user_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

        await self.booking_repository.delete(user.id, id)
        return
