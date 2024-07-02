from fastapi import status
from datetime import date
from typing import Optional
from urllib.parse import urlencode
from uuid import UUID
import httpx
from pydantic import BaseModel
from core.Exceptions import TelegramException, TelegramExceptions

from config import BOOKING_SERVICE_HOST, BOOKING_SERVICE_PORT, BOOKING_SERVICE_VERSION


class BookingFilters(BaseModel):
    game_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    booking_date: Optional[date] = None


class BookingService:
    def __init__(self):
        self.base_url = f"http://{BOOKING_SERVICE_HOST}:{BOOKING_SERVICE_PORT}/api/v{BOOKING_SERVICE_VERSION}"

    async def get_bookings(self, filters: dict = None):
        url = f"{self.base_url}/bookings"

        if filters:
            url += f"?{urlencode(BookingFilters(**filters).model_dump(exclude_unset=True))}"

        print(url)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == status.HTTP_200_OK:
                return response.json()

        raise TelegramException(TelegramExceptions.UNKNOWN_ERROR)

    async def create_booking(self, telegram_id: int, game_id: UUID, booking_date: date):
        url = f"{self.base_url}/bookings"
        headers = {"Telegram-ID": str(telegram_id)}
        payload = {
            "game_id": game_id,
            "booking_date": booking_date.isoformat(),
        }

        print(payload)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == status.HTTP_201_CREATED:
                return response.json()

            print(response.text)
        raise TelegramException(TelegramExceptions.UNKNOWN_ERROR)
