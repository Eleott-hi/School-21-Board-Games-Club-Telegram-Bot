import os
import logging
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL

if __name__ != "__main__":
    from db.models import *


engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """
    Initializes the database by creating all defined models. This function is asynchronous.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """
    Asynchronous function to get a session in a context manager.
    """
    async with async_session() as session:
        yield session


def main():
    """
    A function that initializes the database connection and sets up logging.
    No parameters.
    No return value.
    """
    import models
    import asyncio
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())


if __name__ == "__main__":
    main()