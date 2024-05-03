import os
from models.User import User, Role
# from sqlmodel import SQLModel, select
# from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DB_URL

engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as session:
        await session.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session
