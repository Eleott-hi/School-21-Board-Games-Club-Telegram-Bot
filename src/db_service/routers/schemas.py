from typing import Any, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime


class TestGameWateredDown(BaseModel):
    gameName: str
    maxPlayers: int
    minPlayers: int

class TestState(BaseModel):
    gameName: str
    status: bool

#curl -X POST -H "Content-Type: application/json" -d '{ "gameName": "tratata", "maxPlayers": 5, "minPlayers": 2 }' http://localhost:8000/db/insertgame