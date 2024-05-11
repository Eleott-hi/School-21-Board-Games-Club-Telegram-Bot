import sys
print(sys.path)

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL_TWO
from db.database import get_session
from db.models import *
from main import app
from db.db_data import games


@pytest.fixture(name='session')
async def session_fixture():
    engine = create_async_engine(DB_URL_TWO, echo=True, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


    with async_session as session:
        for game in games:
            try:
                db_game = DbBoardGame.model_validate(game)
                session.add(db_game)
            except Exception as e:
                print(f"error during insertion {e}")
                continue
        session.commit()
        yield session

@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_filtered(client: TestClient):
    response = client.get("/db", 
                        params={"age": 18, "status": "available", \
                                "players_num": 4, "duration": 80, "complexity": "hard", \
                                "genres": ["strategy", "family", "adventure"], \
                                "offset": 0, "limit": 1000}
    )
    data = response.json()

    assert response.status_code == 200
    assert data != []


def test_get_filtered_empty(client: TestClient):
    response = client.get("/db", 
                        params={"age": 1, "status": "available", \
                                "players_num": 4, "duration": 80, "complexity": "hard", \
                                "genres": ["strategy", "family", "adventure"], \
                                "offset": 0, "limit": 1000}
    )
    data = response.json()

    assert response.status_code == 200
    assert data == []

