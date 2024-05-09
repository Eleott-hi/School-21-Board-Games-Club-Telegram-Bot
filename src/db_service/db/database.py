import os
import aioitertools

from sqlmodel import SQLModel, select, and_, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import DB_URL, GOOGLE_TOKEN, AUTHORIZED_USER
from .models import *
from .db_data import games


engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        for game in games:
            try:
                await conn.execute(BoardGame.__table__.insert(), game)
            except Exception as e:
                print(f"error during insertion {e}")
                continue
        await conn.commit()


async def get_session():
    async with async_session() as session:
        yield session


async def get_filtered_games(filters: Filters, conn: AsyncSession):
    conditions = []
    
    if filters.age is not None:
        conditions.append(BoardGame.age <= int(filters.age))

    if filters.status is not None:
        conditions.append(BoardGame.status == filters.status)

    if filters.players_num is not None:
        conditions.append(and_(BoardGame.minPlayers <= int(filters.players_num), 
                               BoardGame.maxPlayers >= int(filters.players_num)))

    if filters.genres:
        genre_conditions = [BoardGame.genre.like(f'%{genre}%') for genre in filters.genres]
        conditions.append(or_(*genre_conditions))

    if filters.complexity:
        conditions.append(BoardGame.gameComplexity == filters.complexity)

    if filters.duration:
        conditions.append(and_(BoardGame.minPlayTime <= int(filters.duration),
                                BoardGame.maxPlayTime >= int(filters.duration)))
        
    offset = filters.offset or 0
    limit = filters.limit or 1000

    stmt = select(BoardGame).where(and_(*conditions)).offset(offset).limit(limit)
    result = await conn.exec(stmt)
    return result.all()
