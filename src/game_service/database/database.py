import logging
import os

from contextlib import asynccontextmanager
from models.Game import Base as booking_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from config.config import POSTGRES_SERVICE_URL


engine = create_async_engine(POSTGRES_SERVICE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

logger = logging.getLogger(__name__)

async def init_db():
    async with engine.begin() as session:
        await session.run_sync(booking_base.metadata.create_all)
        
    # TODO !!! DELETE
    async with async_session() as session:
        from database.test_db import games
        from repositories.games_repository import GamesRepository
        from schemas.schemas import GameRequest

        repository = GamesRepository(session)
        for game in games:
            await repository.create(GameRequest.model_validate(game, strict=False))


# @asynccontextmanager
async def get_session():
    async with async_session() as session:
        logger.info("Session created!")
        yield session
        logger.info ("Session closed")
