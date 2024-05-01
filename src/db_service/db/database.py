import os
import logging
import aioitertools
import gspread


from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .google_parser import GoogleSheetParser
from .config import DB_URL, GOOGLE_TOKEN, AUTHORIZED_USER
from .models import *

engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

def parse_and_convert_data():
    parser = GoogleSheetParser(GOOGLE_TOKEN, AUTHORIZED_USER)
    
    all_values = parser.get_worksheet('table_1', 'sheet1')
    all_values.pop(0)

    games = []
    for val in all_values:
        game = BoardGame(
            gameName = val[1],
            status = False
        )
        games.append(game)
    return games


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
# if you want to insert data into the database from google sheets
        # orm_objects = parse_and_convert_data()
        # for obj in orm_objects:
        #     try:
        #         await conn.execute(obj.__table__.insert(), obj.dict())
        #     except Exception as e:
        #         print(f"error during insertion {e}")
        #         continue
        # await conn.commit()


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
    import asyncio
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())
    
    
if __name__ == "__main__":
    main()