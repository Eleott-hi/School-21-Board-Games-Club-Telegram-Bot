from datetime import date
import logging
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select, update, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from models.Game import Game, GameGenreRelation
from database.database import get_session
from schemas.schemas import GamesFiltersWithGenres, GameRequest

logger = logging.getLogger(__name__)


class GamesRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
    ):
        self.session = session

    async def get(self, id: UUID) -> dict | None:
        q = (
            select(Game, func.array_agg(GameGenreRelation.genre).label("genres"))
            .join(GameGenreRelation, Game.id == GameGenreRelation.game_id)
            .where(Game.id == id)
            .group_by(Game.id)
        )

        try:
            res = (await self.session.execute(q)).first()
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        if res is None:
            raise HTTPException(status_code=404, detail="Game not found")

        res = res._asdict()

        return dict(**res["Game"].asdict(), genres=res["genres"])

    async def get_all(
        self,
        filters: GamesFiltersWithGenres,
    ) -> List[Game]:
        q = select(Game, func.array_agg(GameGenreRelation.genre).label("genres")).join(
            GameGenreRelation, Game.id == GameGenreRelation.game_id
        )

        if filters.title:
            q = q.where(Game.title.ilike(f"%{filters.title}%"))
        if filters.age:
            q = q.where(Game.min_age >= filters.age)
        if filters.players_num:
            q = q.where(Game.min_players <= filters.players_num).where(
                Game.max_players >= filters.players_num
            )
        if filters.duration:
            q = q.where(Game.max_play_time <= filters.duration)
        if filters.complexity:
            q = q.where(Game.complexity == filters.complexity)
        if filters.genres:
            # TODO: add support for multiple genres
            pass

        q = (
            q.group_by(Game.id).order_by(Game.id)
            # .offset(filters.offset)
            # .limit(filters.limit)
        )

        try:
            res = await self.session.execute(q)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        if res is None:
            raise HTTPException(status_code=404, detail="Game not found")

        res = [i._asdict() for i in res]

        return [dict(**i["Game"].asdict(), genres=i["genres"]) for i in res]

    async def create(self, game: GameRequest) -> Game:
        new_game = Game(**game.model_dump(exclude=["genres"]))

        try:
            self.session.add(new_game)
            await self.session.commit()
            await self.session.refresh(new_game)
            await self.create_GGR({new_game.id: game.genres})

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return new_game

    async def delete(self, id: UUID) -> None:
        try:
            await self.session.delete(id)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update(self, id: UUID, game: GameRequest) -> None:
        q = (
            update(Game)
            .where(Game.id == id)
            .values(**game.model_dump(exclude_none=True))
        )

        try:
            await self.session.execute(q)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    # GameGenreRelations
    async def create_GGR(self, GGRdict: dict):
        for game_id, genres in GGRdict.items():
            for genre in genres:
                game_genre_relation = GameGenreRelation(game_id=game_id, genre=genre)
                self.session.add(game_genre_relation)

        await self.session.commit()

    async def get_GGR_by_game_id(self, game_id):
        q = select(GameGenreRelation).where(GameGenreRelation.game_id == game_id)

        try:
            res = await self.session.execute(q)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return res

    async def get_GGR_by_genre(self, genre):
        q = select(GameGenreRelation).where(GameGenreRelation.genre == genre)

        try:
            res = await self.session.execute(q)
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

        return res
