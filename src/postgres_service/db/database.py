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
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


def main():
    import models
    import asyncio
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())


if __name__ == "__main__":
    main()