from models.BaseModel import BaseModel, Base
from uuid import UUID, uuid4
from typing import List
from enum import Enum as PyEnum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as SQLUUID


class Genre(PyEnum):
    ACTION = "action"
    ADVENTURE = "adventure"
    FANTASY = "fantasy"
    HORROR = "horror"
    ROLE_PLAYING = "role-playing"
    STRATEGY = "strategy"
    SUSPENSE = "suspense"
    OTHER = "other"


class GameComplexity(PyEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Game(BaseModel):
    __tablename__ = "games"

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    min_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    min_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    max_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    min_ideal_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    max_ideal_players: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    min_play_time: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    max_play_time: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    rule_time: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    complexity: Mapped[GameComplexity] = mapped_column(
        Enum(GameComplexity), nullable=False
    )
    photo_link: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    video_rules_link: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

class GameGenreRelation(BaseModel):
    __tablename__ = "games_genres_relations"

    game_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("games.id"),
        nullable=False,
    )
    genre: Mapped[Genre] = mapped_column(
        Enum(Genre),
        nullable=False,
    )

    UniqueConstraint('game_id', 'genre', name='game_genre_unique')

