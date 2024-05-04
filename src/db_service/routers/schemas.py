from typing import Any, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, conint, field_validator
from datetime import datetime
from enum import Enum


class Filters(BaseModel):
    age: Optional[conint(ge=0)] = Field(None, description="in years")
    status: Optional[str] = Field(None, description="available/unavailable")
    players_num: Optional[conint(gt=0)] = Field(None, description="string representing int, for example: 10")
    duration: Optional[conint(gt=0)] = Field(None, description="in minutes")
    complexity: Optional[str] = Field(None, description="easy/medium/hard")
    genres: Optional[List[str]] = Field(None, description="Party/Horror/Family/Strategy/Adventure")
