# Бэк для бронирования игр

# игры будем дронировать по суткам (от идеи бронировать по часам - отказались)
# мин ендпоинты (все ендпоинты можно менять/добавлять на свое усмотрение, главное чтоб оставалась логика и здравый смысл):
# ГЕТ /bookings?game={id}&date_from{date}&date_to{date} - список броней на игру с ИД в указанные даты, если нет дат - можно пока что отправить все брони на эту игру.
# ПОСТ /bookings --body {game_id: id, date_from: date, game_to: date} - бронирование игры на дату
# можно добавить обычный КРУД на брони

# Структура БД модели:
# ИД
# ИД игры
# Дата от
# Дата до
# ИД пользователя (в условиях телеграм бота - берется телеграм ИД пользователя из хэдэра + делается запрос в сервис авторизации /api/v1/telegram/user/, при ошибке - статус код 401, норм 200)

from datetime import date
import logging
from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Header, status, Depends, Query
from dependencies.auth_dependency import get_user_by_telegram_id_dependency
from schemas.schemas import BookingRequest, BookingFilters, BookingResponse, User
from services.booking_service import BookingService

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/bookings",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def get_all_bookings_with_filters(
    filters: BookingFilters = Depends(),
    booking_service: BookingService = Depends(),
) -> List[BookingResponse]:
    logger.debug(filters)
    res = await booking_service.get_all(filters)
    return res


@router.get(
    "/bookings/{booking_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def get_booking_by_id(
    booking_id: UUID,
    booking_service: BookingService = Depends(),
) -> BookingResponse:
    res = await booking_service.get(booking_id)
    return res


@router.post(
    "/bookings",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def create_booking(
    booking: BookingRequest,
    user: User = Depends(get_user_by_telegram_id_dependency),
    booking_service: BookingService = Depends(),
) -> BookingResponse:
    new_booking = await booking_service.create(user, booking)
    return new_booking


@router.put(
    "/bookings/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def update_booking(
    booking_id: UUID,
    booking: BookingRequest,
    user: User = Depends(get_user_by_telegram_id_dependency),
    booking_service: BookingService = Depends(),
) -> None:
    await booking_service.update(user, booking_id, booking)


@router.delete(
    "/bookings/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_404_NOT_FOUND: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {},
        status.HTTP_504_GATEWAY_TIMEOUT: {},
    },
)
async def delete_booking(
    booking_id: UUID,
    user: User = Depends(get_user_by_telegram_id_dependency),
    booking_service: BookingService = Depends(),
) -> None:
    await booking_service.delete(user, booking_id)
