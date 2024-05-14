from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from models.User import AuthMethod


class RegisterSchema(BaseModel):
    telegram_id: int
    nickname: str = Field(min_length=3, pattern="^[a-z]+$")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "telegram_id": 12345,
                    "nickname": "pintoved",
                }
            ]
        }
    }


class ConfirmSchema(BaseModel):
    token: str


class User(BaseModel):
    id: UUID
    telegram_id: int
    nickname: str
    email: EmailStr
    auth_method: AuthMethod

    class Config:
        from_attributes = True
