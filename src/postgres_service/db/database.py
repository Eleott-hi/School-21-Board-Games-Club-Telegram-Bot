import os
import logging
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import gspread
import google_parser as gp

from config import DB_URL, GOOGLE_TOKEN, AUTHORIZED_USER

if __name__ != "__main__":
    from db.models import *


engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def parse_and_convert_data():
    parser = gp.GoogleSheetParser('/Users/cursebow/.config/gspread/credentials.json',
                                   '/Users/cursebow/.config/gspread/authorized_user.json')
    
    all_values = parser.get_worksheet('table_1', 'sheet1')
    games = []
    for val in all_values:
        game = BoardGame(
            gameName = val[1],
            minPlayers = val[3].split('-')[0],
            maxPlayers = val[3].split('-')[-1],
            minIdealPlayers = val[4].split('-')[0],
            maxIdealPlayers = val[4].split('-')[-1],
            status = "reserved"
        )
        games.append(game)
    print("omg")
    return games

async def init_db():
    """
    Initializes the database by creating all defined models. This function is asynchronous.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        orm_objects = parse_and_convert_data()
        for obj in orm_objects:
            conn.add(obj)
        await conn.commit()


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