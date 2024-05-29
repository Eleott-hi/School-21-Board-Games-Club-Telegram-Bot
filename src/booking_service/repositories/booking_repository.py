from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from models.Booking import Booking
from database.database import get_session
from schemas.schemas import BookingFilters, BookingRequest

logger = logging.getLogger(__name__)


class BookingRepository:
    def __init__(
        self,
        session=Depends(get_session),
    ):
        self.session = session

    async def get(self, booking_id: UUID):
        self.session.execute(select(Booking).where(Booking.id == booking_id))
        return Booking(
            id=booking_id,
            game_id=booking_id,
            user_id=booking_id,
            booking_date=date.today(),
        )

    async def get_all(self, filters: BookingFilters) -> List[Booking]:
        return []

    async def create(self, user_id: UUID, booking: BookingRequest) -> None:
        pass

    async def delete(self, user_id: UUID, booking_id: UUID) -> None:
        pass

    async def update(
        self, user_id: UUID, booking_id: UUID, booking: BookingRequest
    ) -> None:
        pass
