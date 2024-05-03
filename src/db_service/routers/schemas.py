from typing import Any, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime


class Filters(BaseModel):
    age: Optional[str] = None
    status: Optional[str] = None
    players_num: Optional[str] = None
    duration: Optional[str] = None
    complexity: Optional[str] = None
    genres: Optional[List[str]] = None

#curl -X POST -H "Content-Type: application/json" -d '{ "gameName": "tratata", "maxPlayers": 5, "minPlayers": 2 }' http://localhost:8000/db/insertgame