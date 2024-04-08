import os
from sqlmodel import SQLModel, select,  and_, or_, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload
from config import DB_URL
from database.initial_data import rooms
from database.Models.Models import Room

engine = create_async_engine(DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async with async_session() as session:
        for r in rooms:
            q = select(Room).where(Room.name == r.name)
            user = (await session.execute(q)).first()
            if not user:
                session.add(r)
                await session.commit()
                await session.refresh(r)


async def get_session():
    async with async_session() as session:
        yield session