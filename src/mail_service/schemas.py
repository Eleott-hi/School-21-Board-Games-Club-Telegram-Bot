from typing import Any, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class AuthMethod(str, Enum):
    NATIVE = "native"
    GOOGLE = "google"
    GITLAB = "gitlab"
    TELEGRAM = "telegram"


class UserInfo(BaseModel):
    id: UUID
    telegram_id: str
    email: EmailStr = Field(pattern=".*@student\.21-school\.ru$")
    auth_method: AuthMethod
    role: Role


class RoomInfoCreate(BaseModel):
    name: str
    location: str
    capacity: int = 4
    min_time: int = 15
    max_time: int = 60
    photo_link: Optional[str]


class RoomInfo(RoomInfoCreate):
    id: UUID


class Interval(BaseModel):
    start_time: datetime
    end_time: datetime

    @model_validator(mode="before")
    def remove_timezone(cls, item: Any) -> Any:
        if isinstance(item, datetime):
            item.replace(tzinfo=None)
        return item


class BookingCreate(Interval):
    room_id: UUID


class BookingInfo(BookingCreate):
    id: UUID
    user_id: UUID


class BookingFullInfo(Interval):
    id: UUID
    user: UserInfo
    room: RoomInfo


class NearestEvents(BaseModel):
    starts_soon: List[BookingFullInfo]
    ends_soon: List[BookingFullInfo]


class EmailInfo(BaseModel):
    email: EmailStr
    message: str
