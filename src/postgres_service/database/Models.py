from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
import sqlalchemy as sa

# class Role(str, Enum):
#     USER = "user"
#     ADMIN = "admin"


# class AuthMethod(str, Enum):
#     NATIVE = "native"
#     GOOGLE = "google"
#     GITLAB = "gitlab"
#     TELEGRAM = "telegram"


# class User(SQLModel, table=True):
#     id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
#     telegram_id: str = Field(unique=True)
#     email: str = Field(unique=True)
#     # email_verified: bool = Field(default=False)

#     auth_method: AuthMethod = Field(default=AuthMethod.TELEGRAM)
#     role: Role = Field(default=Role.USER)

#     bookings: list["Booking"] = Relationship(back_populates="user")
#     # violations: list["Violation"] = Relationship(back_populates="violations")


# class Room(SQLModel, table=True):
#     id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
#     name: str = Field(unique=True)
#     location: str
#     capacity: int
#     min_time: int
#     max_time: int
#     photo_link: Optional[str]

#     bookings: list["Booking"] = Relationship(back_populates="room")


# class Booking(SQLModel, table=True):
#     id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
#     start_time: datetime
#     end_time: datetime
#     user_id: UUID = Field(foreign_key="user.id")
#     room_id: UUID = Field(foreign_key="room.id")

#     user: User = Relationship(back_populates="bookings")
#     room: Room = Relationship(back_populates="bookings")


# class ViolationType(Enum):
#     ROOM_NOT_USED = "room_not_used"
#     OVERBOOKING = "overbooking"
#     INAPPROPRIATE_USAGE = "inappropriate_usage"


# class Violation(SQLModel, table=True):
#     id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
#     violation_type: ViolationType
#     description: str
#     user_id: UUID = Field(foreign_key="user.id")
#     booking_id: UUID = Field(foreign_key="booking.id")
#     is_active: bool

    # user: list[User] = Relationship(back_populates="user")
    # booking: list[Booking] = Relationship(back_populates="booking")

from sqlmodel import SQLModel, Field

class BoardGames(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    gameName: str
    minPlayers: int
    maxPlayers: int
    minIdealPlayers: int
    maxIdealPlayers: int
    minPlayTime: int
    maxPlayTime: int
    ruleTime: int
    gameComplexity: str
    minAge: int
    year: int
    gameShortDescription: str
    gameFullDescription: str
    coverImageLink: str
    videoRulesLink: str
    genre: str
    status: str