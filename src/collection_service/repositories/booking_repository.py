from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.Booking import Booking
from database.database import get_session
from schemas.schemas import BookingFilters, BookingRequest

logger = logging.getLogger(__name__)


class BookingRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
    ):
        self.session = session

    async def get(self, booking_id: UUID) -> Booking | None:
        q = select(Booking).where(Booking.id == booking_id)

        try:
            res = await self.session.execute(q)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        res = res.scalars().first()
        if res is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        return res

    async def get_all(self, filters: BookingFilters) -> List[Booking]:
        q = select(Booking)
        if filters.user_id:
            q = q.where(Booking.user_id == filters.user_id)
        if filters.game_id:
            q = q.where(Booking.game_id == filters.game_id)
        if filters.from_date:
            q = q.where(Booking.booking_date >= filters.from_date)
        if filters.to_date:
            q = q.where(Booking.booking_date <= filters.to_date)
        try:
            res = await self.session.execute(q)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return res.scalars().all()

    async def create(self, user_id: UUID, booking: BookingRequest) -> Booking:
        try:
            res = await self.get_all(
                filters=BookingFilters(
                    game_id=booking.game_id,
                    from_date=booking.booking_date,
                    to_date=booking.booking_date,
                )
            )

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        if res:
            print(res, flush=True)
            raise HTTPException(status_code=409, detail="Booking already exists")

        new_booking = Booking(**booking.model_dump(), user_id=user_id)

        self.session.add(new_booking)

        try:
            await self.session.commit()
            await self.session.refresh(new_booking)

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return new_booking

    async def delete(
        self,
        booking_id: UUID,
    ) -> None:
        q = delete(Booking).where(Booking.id == booking_id)

        try:
            await self.session.execute(q)
            await self.session.commit()

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update(
        self,
        booking_id: UUID,
        booking: BookingRequest,
    ) -> None:
        q = (
            update(Booking)
            .where(Booking.id == booking_id)
            .values(**booking.model_dump(exclude_none=True))
        )

        try:
            await self.session.execute(q)
            await self.session.commit()

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
