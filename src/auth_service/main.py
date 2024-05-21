from fastapi import FastAPI

from database.database import init_db
from routers.auth_router import router as auth_router


async def lifespan(app):
    await init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Auth Service",
    description="Service to manage authentication and authorization",
    version="0.0.1",
    root_path="/api/v1",
)

app.include_router(auth_router)


@app.get("/")
async def root():
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
