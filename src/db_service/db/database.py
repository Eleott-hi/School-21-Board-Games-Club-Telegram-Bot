import os
import aioitertools

from sqlmodel import SQLModel, select, and_, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from .config import DB_URL, GOOGLE_TOKEN, AUTHORIZED_USER
from .models import *

engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


async def get_filtered_games(filters: Filters, conn: AsyncSession):
    conditions = []
    
    if filters.age is not None:
        conditions.append(DbBoardGame.age <= int(filters.age))

    if filters.status is not None:
        conditions.append(DbBoardGame.status == filters.status)

    if filters.players_num is not None:
        conditions.append(and_(DbBoardGame.minPlayers <= int(filters.players_num), 
                               DbBoardGame.maxPlayers >= int(filters.players_num)))

    if filters.genres:
        genre_conditions = [DbBoardGame.genre.like(f'%{genre}%') for genre in filters.genres]
        conditions.append(or_(*genre_conditions))

    if filters.complexity:
        conditions.append(DbBoardGame.gameComplexity == filters.complexity)

    if filters.duration:
        conditions.append(and_(DbBoardGame.minPlayTime <= int(filters.duration),
                                DbBoardGame.maxPlayTime >= int(filters.duration)))
        
    offset = filters.offset or 0
    limit = filters.limit or 1000

    stmt = select(DbBoardGame).where(and_(*conditions)).offset(offset).limit(limit)
    result = await conn.exec(stmt)
    return result.all()
