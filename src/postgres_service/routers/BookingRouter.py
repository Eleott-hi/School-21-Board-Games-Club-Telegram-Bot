from typing import List
from fastapi import APIRouter, status, HTTPException, Depends


from routers.schemas import (
    BookingCreate,
    BookingFullInfo,
    BookingInfo,
    NearestEvents,
    RoomInfo,
    UserInfo,
    to_booking_full_info,
)
from database.Models.Models import Role, User, Room, Booking, Violation
from database.database import get_session, AsyncSession, selectinload, select, and_, or_

from uuid import UUID
from services.utils import get_overlap_bookings, get_user, check_booking
from datetime import datetime, timedelta, UTC

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/", status_code=201)
async def create_booking(
    booking: BookingCreate,
    user: UserInfo = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    q = select(Room).where(Room.id == booking.room_id)
    room = (await session.exec(q)).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room with this ID not found",
        )

    if user.role != Role.ADMIN:
        await check_booking(booking, room, user, session)

    overlaps: List[Booking] = await get_overlap_bookings(
        room.id, booking.start_time, booking.end_time, session
    )

    if overlaps != []:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked in this time",
        )

    booking = Booking(user_id=user.id, **booking.__dict__)
    session.add(booking)
    await session.commit()
    await session.refresh(booking)


@router.delete("/{id}", status_code=204)
async def delete_booking(
    id: UUID,
    user: UserInfo = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    q = select(Booking).where(Booking.id == id)
    booking = (await session.exec(q)).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking with this ID not found",
        )

    if booking.user_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this booking",
        )

    min_15_from_now = datetime.now(tz=None) + timedelta(minutes=15)
    if booking.start_time <= min_15_from_now and user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can not delete booking already",
        )

    await session.delete(booking)
    await session.commit()


@router.get("/nearest_events")
async def get_nearest_events(
    session: AsyncSession = Depends(get_session),
):
    now = datetime.now(tz=None)
    after_15_min = now + timedelta(minutes=15)

    q = (
        select(Booking)
        .where(
            or_(
                and_(now <= Booking.start_time, Booking.start_time <= after_15_min),
                and_(now <= Booking.end_time, Booking.end_time <= after_15_min),
            )
        )
        .options(selectinload(Booking.user), selectinload(Booking.room))
    )

    bookings = (await session.exec(q)).all()

    starts_soon = [
        to_booking_full_info(b) for b in bookings if now <= b.start_time <= after_15_min
    ]
    ends_soon = [
        to_booking_full_info(b) for b in bookings if now <= b.end_time <= after_15_min
    ]

    # print()
    # print()
    # print(starts_soon)
    # print()
    # print(ends_soon)
    # print(ends_soon[0].user)
    # print()
    # print()

    return NearestEvents(starts_soon=starts_soon, ends_soon=ends_soon)


@router.get("/", response_model=List[BookingInfo])
async def get_booking_list(
    user: UserInfo = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    q = select(Booking)
    bookings = (await session.exec(q)).all()

    return bookings


@router.get("/by_user", response_model=List[BookingInfo])
async def get_booking_list_by_user(
    user: UserInfo = Depends(get_user),
    session: AsyncSession = Depends(get_session),
):
    q = select(Booking).where(Booking.user_id == user.id)
    bookings = (await session.exec(q)).all()

    return bookings