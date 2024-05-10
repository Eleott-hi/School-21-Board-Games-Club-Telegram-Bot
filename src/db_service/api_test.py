from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from db.database import get_session
from .main import app


def test_get_filtered():
    client = TestClient(app)
    response = client.get("/db", 
                          json={"age": 18, "status": "available", \
                                "players_num": 4, "duration": 80, "complexity": "hard", \
                                "genres": ["strategy", "family", "adventure"], \
                                "offset": 0, "limit": 1000}
    )
    data = response.json()

    assert response.status_code == 200
    assert data != []

    response = client.get("/db", 
                          json={"age": 1, "status": "available", \
                                "players_num": 4, "duration": 80, "complexity": "hard", \
                                "genres": ["strategy", "family", "adventure"], \
                                "offset": 0, "limit": 1000}
    )
    data = response.json()

    assert response.status_code == 200
    assert data == []