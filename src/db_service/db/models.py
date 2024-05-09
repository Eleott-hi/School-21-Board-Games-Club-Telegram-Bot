from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, Boolean

class BoardGame(SQLModel):
    title: Optional[str]
    description: Optional[str]
    minPlayers: Optional[int]
    maxPlayers: Optional[int]
    minIdealPlayers: Optional[int]
    maxIdealPlayers: Optional[int]
    minPlayTime: Optional[int]
    maxPlayTime: Optional[int]
    ruleTime: Optional[int]
    gameComplexity: Optional[str]
    age: Optional[int]
    year: Optional[int]
    gameShortDescription: Optional[str]
    gameFullDescription: Optional[str]
    coverImageLink: Optional[str]
    videoRulesLink: Optional[str]
    genre: Optional[str]
    status: Optional[str] = Field(default="available")
    photo_link: Optional[str]


class DbBoardGame(BoardGame, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)




class Filters(SQLModel):
    # age: Optional[conint(ge=0)] = Field(None, description="in years")
    # status: Optional[str] = Field(None, description="available/unavailable")
    # players_num: Optional[conint(gt=0)] = Field(None, description="string representing int, for example: 10")
    # duration: Optional[conint(gt=0)] = Field(None, description="in minutes")
    # complexity: Optional[str] = Field(None, description="easy/medium/hard")
    # genres: Optional[List[str]] = Field(None, description="Party/Horror/Family/Strategy/Adventure")
    # offset: Optional[conint(gt=0)] = Field(None, description="offset")
    # limit: Optional[conint(gt=0)] = field(None, description="returned count")

    age: Optional[int] = Field(None, description="in years")
    status: Optional[str] = Field(None, description="available/unavailable")
    players_num: Optional[int] = Field(None, description="string representing int, for example: 10")
    duration: Optional[int] = Field(None, description="in minutes")
    complexity: Optional[str] = Field(None, description="easy/medium/hard")
    genres: Optional[List[str]] = Field(None, description="Party/Horror/Family/Strategy/Adventure")
    offset: Optional[int] = Field(None, description="offset")
    limit: Optional[int] = Field(None, description="returned count")

