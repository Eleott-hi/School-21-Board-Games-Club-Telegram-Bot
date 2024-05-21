from uuid import UUID, uuid4
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import UUID as SQLUUID

Base = declarative_base()

class Role(str, PyEnum):
    USER = "user"
    ADMIN = "admin"

class AuthMethod(str, PyEnum):
    NATIVE = "native"
    GOOGLE = "google"
    GITLAB = "gitlab"
    TELEGRAM = "telegram"

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    nickname: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    auth_method: Mapped[AuthMethod] = mapped_column(Enum(AuthMethod), default=AuthMethod.TELEGRAM)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
