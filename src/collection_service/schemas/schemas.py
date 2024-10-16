from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime
from enum import Enum as PyEnum

from models.Collection import CollectionType


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


class CollectionFilters(BaseModel):
    game_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    type: Optional[CollectionType] = None


class CollectionRequest(BaseModel):
    game_id: UUID
    type: CollectionType


class CollectionResponse(BaseModel):
    id: UUID
    user_id: UUID
    game_id: UUID
    type: CollectionType
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FastapiError(BaseModel):
    detail: str
