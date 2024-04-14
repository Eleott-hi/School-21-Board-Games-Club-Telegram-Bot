from typing import Any, List, Optional
from uuid import UUID
from database.Models.Models import AuthMethod, Role, ViolationType
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime


class UserInfo(BaseModel):
    id: UUID
    telegram_id: str
    email: EmailStr = Field(pattern=".*@student\.21-school\.ru$")
    auth_method: AuthMethod
    role: Role

