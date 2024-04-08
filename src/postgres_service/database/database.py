import os
import logging
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append("..")
from config import DB_URL
from Models import *

print(DB_URL)
engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


async def main():
    logging.debug("Main function executed")
    await init_db()
    logging.debug("Main function executed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())