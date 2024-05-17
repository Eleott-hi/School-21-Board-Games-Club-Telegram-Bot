from fastapi import FastAPI
import sys
from contextlib import asynccontextmanager

from db.database import init_db
from routers.selection_router import router as selection_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await init_db()
    yield

app = FastAPI(
    lifespan=lifespan,
    root_path="/postgres_service",
)

app.include_router(selection_router)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
