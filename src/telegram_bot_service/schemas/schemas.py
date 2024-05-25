from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum as PyEnum

class TelegramMessageToUser(BaseModel):
    chat_id: int
    text: str
