import os
import aioitertools

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import DB_URL, GOOGLE_TOKEN, AUTHORIZED_USER
from .models import *
from .db_data import games

from routers.schemas import Filters


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


async def get_filtered_games(filters: Filters) -> BoardGame:
    filter_values = {k: v for k, v in filters.dict().items() if v is not None}
    board_game = BoardGame(**filter_values)
    stmt = select(board_game)
    result = await get_session().exec(stmt)
    result_data = result.all()
    return result_data