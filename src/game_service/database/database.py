import logging
import os

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from config.config import POSTGRES_SERVICE_URL


engine = create_async_engine(POSTGRES_SERVICE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

logger = logging.getLogger(__name__)


# @asynccontextmanager
async def get_session():
    async with async_session() as session:
        logger.info("Session created!")
        yield session
        logger.info("Session closed")
