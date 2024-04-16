from fastapi import FastAPI
import sys

from db.database import init_db
from contextlib import asynccontextmanager
from routers.selection_router import router as selection_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    lifespan=lifespan,
    root_path="/postgres_service",
)

app.include_router(selection_router)

if __name__ == "__main__":
    import uvicorn

# investigation (TO BE DELETED)
    modnames: tuple = sys.builtin_module_names
    print ("BUILT-IN MODULES")
    for name in modnames:
        print(name)
#investigation
        

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
