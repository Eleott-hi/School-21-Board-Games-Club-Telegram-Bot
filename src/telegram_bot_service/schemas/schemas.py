from uuid import UUID
from pydantic import BaseModel, EmailStr
from enum import Enum as PyEnum


class TelegramMessageToUser(BaseModel):
    chat_id: int
    text: str


class AuthMethod(str, PyEnum):
    NATIVE = "native"
    GOOGLE = "google"
    GITLAB = "gitlab"
    TELEGRAM = "telegram"


class User(BaseModel):
    id: UUID
    telegram_id: int
    nickname: str
    email: EmailStr
    auth_method: AuthMethod
