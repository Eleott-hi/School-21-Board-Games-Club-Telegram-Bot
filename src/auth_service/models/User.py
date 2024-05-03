from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class AuthMethod(str, Enum):
    NATIVE = "native"
    GOOGLE = "google"
    GITLAB = "gitlab"
    TELEGRAM = "telegram"


class User(Base):
    __tablename__ = "users"

    id: Mapper

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    telegram_id: str = Field(unique=True)
    email: str = Field(unique=True)

    auth_method: AuthMethod = Field(default=AuthMethod.TELEGRAM)
    role: Role = Field(default=Role.USER)
