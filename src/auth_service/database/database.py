import os

from contextlib import asynccontextmanager
from models.User import Base as user_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from config import POSTGRES_SERVICE_URL

engine = create_async_engine(POSTGRES_SERVICE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(user_base.metadata.create_all)


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session
