import sqlalchemy as sa
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

class BoardGame(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    gameName: str
    minPlayers: int
    maxPlayers: int
    minIdealPlayers: int
    maxIdealPlayers: int
    minPlayTime: int
    maxPlayTime: int
    ruleTime: int
    gameComplexity: str
    minAge: int
    year: int
    gameShortDescription: str
    gameFullDescription: str
    coverImageLink: str
    videoRulesLink: str
    genre: str
    status: str
