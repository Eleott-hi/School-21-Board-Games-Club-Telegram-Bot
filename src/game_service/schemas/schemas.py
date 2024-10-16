from typing import List, Optional
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime
from enum import Enum as PyEnum
from models.Game import GameComplexity, Genre


class GameRequest(BaseModel):
    title: str
    year: int
    min_age: int
    min_players: int
    max_players: int
    min_ideal_players: int
    max_ideal_players: int
    min_play_time: int
    max_play_time: int
    rule_time: int
    photo_link: str
    genres: List[Genre]
    complexity: GameComplexity
    description: Optional[str] = None
    video_rules_link: Optional[str] = None
    note: Optional[str] = None
    tesera_link: Optional[str] = None
    shop_link: Optional[str] = None
    owner: Optional[str] = None




class GameResponse(GameRequest):
    id: UUID


class GamesFiltersWithoutGenres(BaseModel):
    offset: int = 0
    limit: int = 1000000000
    title: Optional[str] = None
    age: Optional[int] = None
    players_num: Optional[int] = None
    duration: Optional[int] = None
    complexity: Optional[GameComplexity] = None


class GamesFiltersWithGenres(BaseModel):
    offset: int = 0
    limit: int = 10
    title: Optional[str] = None
    age: Optional[int] = None
    players_num: Optional[int] = None
    duration: Optional[int] = None
    complexity: Optional[GameComplexity] = None
    genres: Optional[List[Genre]] = None
